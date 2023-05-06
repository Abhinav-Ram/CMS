from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
import os
from datetime import datetime

base_dir = basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


def connect_db(app, database):
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, database)
    db.init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return db


class FoodItem(db.Model):
    __tablename__ = 'food_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<FoodItem {self.name} {self.price}>'


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.String(80), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    PrimaryKeyConstraint(id, item_id, name="one_on_one")

    def __repr__(self):
        return f'<CartItem {self.id} {self.name} {self.price} {self.qty}>'

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    

    def __repr__(self):
        return f'<Order {self.id} {self.date}>'