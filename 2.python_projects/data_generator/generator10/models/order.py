from models.basemodel import BaseModel, check_model_implementation


class Order(BaseModel):
    def __init__(self, id, order_at, store_id, user_id):
        self.id = id
        self.order_at = order_at
        self.store_id = store_id
        self.user_id = user_id

    def print_data(self):
        print(f"Id: {self.id}")
        print(f"Order At: {self.order_at}")
        print(f"Store Id: {self.store_id}")
        print(f"User Id: {self.user_id}")
        print()

    def get_row(self):
        return [self.id, self.order_at, self.store_id, self.user_id]

    @staticmethod
    def get_csv_filename():
        return "order.csv"

    @staticmethod
    def get_csv_header():
        return ['Id', 'OrderAt', 'StoreId', 'UserId']

    def __str__(self):
        return f"Id: {self.id}, Order At: {self.order_at}, Store Id: {self.store_id}, User Id: {self.user_id}"

check_model_implementation(Order)
