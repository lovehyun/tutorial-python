# 타입이 추가될 때도 아주 간결하게 관리 가능!
# if-elif을 아예 없앨 수 있음.
class DisplayData:
    def __init__(self, data):
        self.handlers = {
            str: self.display_str,
            list: self.display_list,
            dict: self.display_dict
        }
        handler = self.handlers.get(type(data), self.unsupported_type)
        handler(data)

    def display_str(self, data):
        print(f"문자열: {data}")

    def display_list(self, data):
        print(f"리스트: {data}")

    def display_dict(self, data):
        print(f"딕셔너리: {data}")

    def unsupported_type(self, data):
        print("지원하지 않는 타입입니다.")

DisplayData("world")           # 문자열: world
DisplayData([4, 5, 6])         # 리스트: [4, 5, 6]
DisplayData({"x": 10, "y": 20}) # 딕셔너리: {'x': 10, 'y': 20}
