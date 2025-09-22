#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza
from extensions import db

with app.app_context():
    db.create_all()

fake = Faker()

def setup_database():
    with app.app_context():
        print("Setting up database...")
        
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("Tables created successfully!")
        
        # Create restaurants
        restaurants = []
        restaurants.append(Restaurant(name="Karen's Pizza Shack", address="address1"))
        restaurants.append(Restaurant(name="Sanjay's Pizza", address="address2"))
        restaurants.append(Restaurant(name="Kiki's Pizza", address="address3"))
        
        # Add more restaurants with random data
        for i in range(7):
            restaurant = Restaurant(
                name=f"{fake.first_name()}'s Pizza",
                address=f"address{i+4}"
            )
            restaurants.append(restaurant)
        
        db.session.add_all(restaurants)
        db.session.commit()
        print(f"Created {len(restaurants)} restaurants")
        
        # Create pizzas
        pizzas = []
        pizzas.append(Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese"))
        pizzas.append(Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"))
        pizzas.append(Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard"))
        
        # Add more pizzas
        pizza_names = ["Margherita", "Hawaiian", "Meat Lovers", "Veggie Supreme", "BBQ Chicken", "White Pizza", "Buffalo Chicken"]
        base_ingredients = ["Dough", "Tomato Sauce", "Cheese"]
        extra_ingredients = ["Pepperoni", "Sausage", "Mushrooms", "Bell Peppers", "Onions", "Olives", "Pineapple", "Ham", "Chicken", "Spinach", "Garlic", "Basil"]
        
        for name in pizza_names:
            ingredients = base_ingredients.copy()
            # Add 1-4 random extra ingredients
            num_extras = randint(1, 4)
            selected_extras = fake.random_elements(elements=extra_ingredients, length=num_extras, unique=True)
            ingredients.extend(selected_extras)
            
            pizza = Pizza(
                name=name,
                ingredients=", ".join(ingredients)
            )
            pizzas.append(pizza)
        
        db.session.add_all(pizzas)
        db.session.commit()
        print(f"Created {len(pizzas)} pizzas")
        
        # Create restaurant_pizzas relationships
        restaurant_pizzas = []
        
        # Create the specific relationship for testing (Emma pizza at Karen's Pizza Shack for $1)
        restaurant_pizzas.append(RestaurantPizza(
            price=1,
            restaurant_id=1,  # Karen's Pizza Shack
            pizza_id=1        # Emma
        ))
        
        # Create random relationships
        for _ in range(30):
            restaurant_pizza = RestaurantPizza(
                price=randint(1, 30),
                restaurant_id=rc(restaurants).id,
                pizza_id=rc(pizzas).id
            )
            restaurant_pizzas.append(restaurant_pizza)
        
        # Remove duplicates (same restaurant-pizza combination)
        unique_pairs = set()
        unique_restaurant_pizzas = []
        
        for rp in restaurant_pizzas:
            pair = (rp.restaurant_id, rp.pizza_id)
            if pair not in unique_pairs:
                unique_pairs.add(pair)
                unique_restaurant_pizzas.append(rp)
        
        db.session.add_all(unique_restaurant_pizzas)
        db.session.commit()
        
        print(f"Created {len(unique_restaurant_pizzas)} restaurant-pizza relationships")
        print("Database setup completed successfully!")
        
        # Verify the data
        print("\nVerification:")
        print(f"Total restaurants: {Restaurant.query.count()}")
        print(f"Total pizzas: {Pizza.query.count()}")
        print(f"Total restaurant-pizza relationships: {RestaurantPizza.query.count()}")

if __name__ == '__main__':
    setup_database()