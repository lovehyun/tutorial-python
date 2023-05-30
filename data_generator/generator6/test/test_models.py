import os, sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from models.user import User
from models.store import Store
from models.item import Item

def test_user():
    user = User("Shawn Park", "Male", "1990-01-01", "Address 1")
    print(user)

def test_store():
    store = Store("My Store", "Coffee", "Address 1")
    print(store)

def test_item():
    item = Item("Ice Americano", "Coffee", "5500")
    print(item)

if __name__ == '__main__':
    test_user()
    test_store()
    test_item()
