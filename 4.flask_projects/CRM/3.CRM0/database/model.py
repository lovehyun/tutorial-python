import sqlite3

# SQLite database path
db_path = 'database/user-sample.sqlite'


class Model:
    def __init__(self, table_name):
        self.table_name = table_name

    def execute_query(self, query, fetchall=False):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        if fetchall:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        conn.commit()
        conn.close()
        return result


table_user = 'users'
table_store = 'stores'
table_item = 'items'
table_order = 'orders'
table_orderitem = 'order_items'


class User(Model):
    def __init__(self):
        super().__init__(table_user)

    def create(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            age INTEGER,
            birthdate TEXT,
            address TEXT
        );
        '''
        self.execute_query(query)


class Store(Model):
    def __init__(self):
        super().__init__(table_store)

    def create(self):
        query = '''
        CREATE TABLE IF NOT EXISTS stores (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            address TEXT
        );
        '''
        self.execute_query(query)


class Item(Model):
    def __init__(self):
        super().__init__(table_item)

    def create(self):
        query = '''
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            unitprice TEXT
        );
        '''
        self.execute_query(query)


class Order(Model):
    def __init__(self):
        super().__init__(table_order)

    def create(self):
        query = '''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            orderat TEXT,
            storeid TEXT,
            userid TEXT,
            FOREIGN KEY (storeid) REFERENCES stores (id),
            FOREIGN KEY (userid) REFERENCES users (id)
        );
        '''
        self.execute_query(query)


class OrderItem(Model):
    def __init__(self):
        super().__init__(table_orderitem)

    def create(self):
        query = '''
        CREATE TABLE IF NOT EXISTS order_items (
            id TEXT PRIMARY KEY,
            orderid TEXT,
            itemid TEXT,
            FOREIGN KEY (orderid) REFERENCES orders (id),
            FOREIGN KEY (itemid) REFERENCES items (id)
        );
        '''
        self.execute_query(query)


# Create tables if they don't exist
user_model = User()
user_model.create()

store_model = Store()
store_model.create()

item_model = Item()
item_model.create()

order_model = Order()
order_model.create()

order_item_model = OrderItem()
order_item_model.create()
