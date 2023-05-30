class Order:
    def __init__(self, id, order_at, store_id, user_id):
        self.id = id
        self.order_at = order_at
        self.store_id = store_id
        self.user_id = user_id

    def __str__(self):
        return f"Id: {self.id}, Order At: {self.order_at}, Store Id: {self.store_id}, User Id: {self.user_id}"
