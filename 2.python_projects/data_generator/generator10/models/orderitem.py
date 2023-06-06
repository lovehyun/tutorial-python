from models.basemodel import BaseModel, check_model_implementation


class OrderItem(BaseModel):
    def __init__(self, id, order_id, item_id):
        self.id = id
        self.order_id = order_id
        self.item_id = item_id

    def print_data(self):
        print(f"Id: {self.id}")
        print(f"Order Id: {self.order_id}")
        print(f"Item Id: {self.item_id}")
        print()

    def get_row(self):
        return [self.id, self.order_id, self.item_id]

    @staticmethod
    def get_csv_filename():
        return "orderitem.csv"

    @staticmethod
    def get_csv_header():
        return ['Id', 'OrderId', 'ItemId']

    def __str__(self):
        return f"Id: {self.id}, Order Id: {self.order_id}, Item Id: {self.item_id}"

check_model_implementation(OrderItem)
