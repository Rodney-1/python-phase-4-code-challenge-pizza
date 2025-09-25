#!/usr/bin/env python3

from extensions import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', lazy=True)

    def to_dict(self, only=None):
        data = {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }
        if 'restaurant_pizzas' in (only or []):
            data['restaurant_pizzas'] = [rp.to_dict(only=('id', 'price', 'pizza_id', 'restaurant_id')) for rp in self.restaurant_pizzas]
        if only:
            return {k: v for k, v in data.items() if k in only}
        return data


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', lazy=True)

    def to_dict(self, only=None):
        data = {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }
        if only:
            return {k: v for k, v in data.items() if k in only}
        return data


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    def __init__(self, **kwargs):
        if 'price' in kwargs and not (1 <= kwargs['price'] <= 30):
            raise ValueError("Price must be between 1 and 30")
        super().__init__(**kwargs)

    def to_dict(self, only=None):
        data = {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id
        }
        if 'pizza' in (only or []) or not only:
            data['pizza'] = self.pizza.to_dict() if self.pizza else None
        if 'restaurant' in (only or []) or not only:
            data['restaurant'] = self.restaurant.to_dict() if self.restaurant else None
        if only:
            return {k: v for k, v in data.items() if k in only}
        return data


def add_sample_data():
    """Add sample data to the database"""
    from app import app
    with app.app_context():
        print("Adding sample data...")
        
        # Create restaurants
        restaurant1 = Restaurant(name="Karen's Pizza Shack", address="address1")
        restaurant2 = Restaurant(name="Sanjay's Pizza", address="address2")
        restaurant3 = Restaurant(name="Kiki's Pizza", address="address3")
        
        db.session.add_all([restaurant1, restaurant2, restaurant3])
        db.session.commit()
        print("Added restaurants")
        
        # Create pizzas
        pizza1 = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
        pizza2 = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        pizza3 = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
        
        db.session.add_all([pizza1, pizza2, pizza3])
        db.session.commit()
        print("Added pizzas")
        
        # Create restaurant-pizza relationships
        rp1 = RestaurantPizza(price=1, restaurant_id=restaurant1.id, pizza_id=pizza1.id)
        rp2 = RestaurantPizza(price=15, restaurant_id=restaurant2.id, pizza_id=pizza2.id)
        rp3 = RestaurantPizza(price=20, restaurant_id=restaurant3.id, pizza_id=pizza3.id)
        
        db.session.add_all([rp1, rp2, rp3])
        db.session.commit()
        print("Added restaurant-pizza relationships")
        
        # Verify data
        print(f"Total restaurants: {Restaurant.query.count()}")
        print(f"Total pizzas: {Pizza.query.count()}")
        print(f"Total restaurant-pizza relationships: {RestaurantPizza.query.count()}")
        
        print("Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()