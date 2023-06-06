class OrderItem:
    def __init__(self, id, order_id, item_id):
        self.id = id
        self.order_id = order_id
        self.item_id = item_id

    def __str__(self):
        return f"Id: {self.id}, Order Id: {self.order_id}, Item Id: {self.item_id}"
