from generators.generator import Generator, register_generator

from generators.common.address_generator import AddressGenerator
from generators.store.storename_generator import StoreNameGenerator

from models.store import Store


@register_generator("store")
class StoreGenerator(Generator):
    def __init__(self):
        self.address_generator = AddressGenerator()
        self.storename_generator = StoreNameGenerator()

    def generate(self):
        store_type = self.storename_generator.generate_type()
        name = self.storename_generator.generate_name(store_type)
        address = self.address_generator.generate()
        return Store(name, store_type, address)
