from flask_sqlalchemy import SQLAlchemy


# choose DB ORM
db = SQLAlchemy()

table_user = 'users'
table_store = 'stores'
table_item = 'items'
table_order = 'orders'
table_orderitem = 'order_items'


class User(db.Model):
    __tablename__ = table_user
    # setup column
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(16))
    gender = db.Column(db.String(16))
    age = db.Column(db.Integer())
    birthdate = db.Column(db.String(32))
    address = db.Column(db.String(64))
    # setup relation
    orderR = db.relationship('Order', backref='users')


class Store(db.Model):
    __tablename__ = table_store
    # setup column
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(32))
    type = db.Column(db.String(32))
    address = db.Column(db.String(64))
    # setup relation
    orderR = db.relationship('Order', backref='stores')


class Item(db.Model):
    __tablename__ = table_item
    # setup column
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(32))
    type = db.Column(db.String(32))
    unitprice = db.Column(db.String(16))
    # setup relation
    orderItemR = db.relationship('OrderItem', backref='items')


class Order(db.Model):
    __tablename__ = table_order
    # setup column
    id = db.Column(db.String(64), primary_key=True)
    orderat = db.Column(db.String(64))
    storeid = db.Column(db.String(64), db.ForeignKey(table_store + '.id'))
    userid = db.Column(db.String(64), db.ForeignKey(table_user + '.id'))
    # setup relation
    orderItemR = db.relationship('OrderItem', backref='orders')


class OrderItem(db.Model):
    __tablename__ = table_orderitem
    # setup column
    id = db.Column(db.String(64), primary_key=True)
    orderid = db.Column(db.String(64), db.ForeignKey(table_order + '.id'))
    itemid = db.Column(db.String(64), db.ForeignKey(table_item + '.id'))
