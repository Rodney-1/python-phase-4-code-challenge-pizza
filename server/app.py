#!/usr/bin/env python3
# server/app.py
import os
from flask import Flask, request, make_response
from flask_migrate import Migrate
from extensions import db
from models import Restaurant, Pizza, RestaurantPizza

# import routes or create_app logic here


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def home():
    return '<h1>Code Challenge: Pizza Restaurants</h1>'


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurants_data = [restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants]
    return make_response(restaurants_data, 200)


@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response({'error': 'Restaurant not found'}, 404)
    
    restaurant_data = restaurant.to_dict(only=('id', 'name', 'address', 'restaurant_pizzas'))
    return make_response(restaurant_data, 200)


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response({'error': 'Restaurant not found'}, 404)
    
    db.session.delete(restaurant)
    db.session.commit()
    
    return make_response('', 204)


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizzas_data = [pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas]
    return make_response(pizzas_data, 200)


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
            return make_response({'errors': ['Missing required fields']}, 400)
        
        # Check if restaurant and pizza exist
        restaurant = Restaurant.query.get(data['restaurant_id'])
        pizza = Pizza.query.get(data['pizza_id'])
        
        if not restaurant:
            return make_response({'errors': ['Restaurant not found']}, 400)
        
        if not pizza:
            return make_response({'errors': ['Pizza not found']}, 400)
        
        # Create new RestaurantPizza
        restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        
        db.session.add(restaurant_pizza)
        db.session.commit()
        
        # Return the created RestaurantPizza with related data
        response_data = restaurant_pizza.to_dict(only=('id', 'price', 'pizza_id', 'restaurant_id', 'pizza', 'restaurant'))
        return make_response(response_data, 201)
        
    except ValueError as e:
        db.session.rollback()
        return make_response({'errors': ["validation errors"]}, 400)
    except Exception as e:
        db.session.rollback()
        return make_response({'errors': ['Failed to create RestaurantPizza']}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)