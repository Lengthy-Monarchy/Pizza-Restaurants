from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config.from_object('config.Config')  # config.py file with the class Config

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Pizza Restaurant API!'})

# Error handling for not found and unexpected errors
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id, description="Restaurant not found")
    pizzas = [{'id': rp.pizza.id, 'name': rp.pizza.name, 'ingredients': rp.pizza.ingredients} for rp in restaurant.pizzas]
    return jsonify({'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address, 'pizzas': pizzas})

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id, description="Restaurant not found")
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({}), 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def add_restaurant_pizza():
    data = request.json
    if not data or 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
        abort(400, description="Invalid data provided.")
    new_restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
    db.session.add(new_restaurant_pizza)
    db.session.commit()
    return jsonify({'id': new_restaurant_pizza.pizza.id, 'name': new_restaurant_pizza.pizza.name, 'ingredients': new_restaurant_pizza.pizza.ingredients}), 201

if __name__ == '__main__':
    app.run(debug=True)
