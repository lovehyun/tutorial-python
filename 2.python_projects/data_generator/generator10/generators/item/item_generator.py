import random
import uuid

from generators.generator import Generator, register_generator

from models.item import Item


@register_generator("item")
class ItemGenerator(Generator):
    def __init__(self):
        self.item_types = {
            "Coffee": {
                "Americano": 3000,
                "Latte": 4000,
                "Espresso": 2500,
                "Cappuccino": 4500,
                "Mocha": 5000
            },
            "Juice": {
                "Orange": 2000,
                "Apple": 2500,
                "Grape": 3000,
                "Pineapple": 3500,
                "Watermelon": 4000
            },
            "Cake": {
                "Chocolate": 6000,
                "Strawberry": 5500,
                "Vanilla": 5000,
                "Red Velvet": 6500,
                "Carrot": 6000
            }
        }

    def generate(self, item_type=None):
        item_id = uuid.uuid4()

        if item_type is None:
            item_type = random.choice(list(self.item_types.keys()))

        item_subtype = random.choice(list(self.item_types[item_type].keys()))
        unit_price = self.item_types[item_type][item_subtype]
        item_name = f"{item_subtype} {item_type}"
        return Item(item_id, item_name, item_type, unit_price)

    def generate_coffee(self):
        return self.generate("Coffee")

    def generate_juice(self):
        return self.generate("Juice")

    def generate_cake(self):
        return self.generate("Cake")