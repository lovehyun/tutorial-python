# 기본 가장 쉬운 if-else 패턴
class DisplayData:
    def __init__(self, data):
        
        # if type(data) == str:
        if isinstance(data, str):
            self.display_str(data)
        # elif type(data) == list:
        elif isinstance(data, list):
            self.display_list(data)
        elif isinstance(data, dict):
            self.display_dict(data)
        else:
            raise TypeError("지원하지 않는 타입입니다.")

    def display_str(self, data):
        print(f"문자열: {data}")

    def display_list(self, data):
        print(f"리스트: {data}")

    def display_dict(self, data):
        print(f"딕셔너리: {data}")

DisplayData("hello")           # 문자열: hello
DisplayData([1, 2, 3])         # 리스트: [1, 2, 3]
DisplayData({"a": 1, "b": 2})  # 딕셔너리: {'a': 1, 'b': 2}
