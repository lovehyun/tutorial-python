import random
import uuid

from generators.generator import Generator, register_generator

from models.orderitem import OrderItem

from generators.order.read_uuid_from_csv import order_uuids, item_uuids


@register_generator("orderitem")
class OrderItemGenerator(Generator):
    def __init__(self):
        self.order_uuids = order_uuids
        self.item_uuids = item_uuids

    def generate(self):
        order_uuid = self._get_random_order_uuid()
        item_uuid = self._get_random_item_uuid()
        
        orderitem_id = uuid.uuid4()
        return OrderItem(orderitem_id, order_uuid, item_uuid)

    def _get_random_order_uuid(self):
        return random.choice(self.order_uuids)

    def _get_random_item_uuid(self):
        return random.choice(self.item_uuids)
