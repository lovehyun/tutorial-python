import random
import uuid
from datetime import datetime, timedelta

from generators.generator import Generator, register_generator

from models.order import Order

from generators.order.read_uuid_from_csv import user_uuids, store_uuids


@register_generator("order")
class OrderGenerator(Generator):
    def generate(self):
        start = datetime(2023, 1, 1)  # 범위의 시작 날짜
        end = datetime(2023, 12, 31)  # 범위의 끝 날짜

        # 범위 내에서 랜덤한 날짜 생성
        time_difference = end - start
        random_seconds = random.randint(0, time_difference.total_seconds())
        order_at = start + timedelta(seconds=random_seconds)

        user_id = random.choice(user_uuids)
        store_id = random.choice(store_uuids)

        order_id = uuid.uuid4()
        order = Order(order_id, order_at, store_id, user_id)
        return order
