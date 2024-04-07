from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade="all, delete")

    @validates('name')
    def validate_name(self, key, name):
        assert len(name.split()) < 50, 'Name must be less than 50 words'
        return name

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza', cascade="all, delete")

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza = db.relationship('Pizza', back_populates='restaurants')
    restaurant = db.relationship('Restaurant', back_populates='pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise AssertionError('Price must be between 1 and 30')
        return price
