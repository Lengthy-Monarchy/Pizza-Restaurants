from models import db, Restaurant, Pizza, RestaurantPizza
from app import app

def seed_data():
    # Delete existing data
    db.session.query(RestaurantPizza).delete()
    db.session.query(Pizza).delete()
    db.session.query(Restaurant).delete()

    # Adding sample restaurants
    dominion = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
    pizza_hut = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")

    # Adding sample pizzas
    cheese = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")

    db.session.add(dominion)
    db.session.add(pizza_hut)
    db.session.add(cheese)
    db.session.add(pepperoni)

    # Adding sample restaurant pizzas
    db.session.add(RestaurantPizza(price=10, restaurant=dominion, pizza=cheese))
    db.session.add(RestaurantPizza(price=12, restaurant=pizza_hut, pizza=pepperoni))

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
        print("Database seeded!")
