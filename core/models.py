from core import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(255))
    password = db.Column(db.String(100), nullable=False)
    address_1 = db.Column(db.String(255))
    address_2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    pincode = db.Column(db.String(255))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    img_url = db.Column(db.String(255))
    category = db.Column(db.String(255))
    inventory = db.Column(db.Integer)
    price = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.Date)
    total = db.Column(db.Integer)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)