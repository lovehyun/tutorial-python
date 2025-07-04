# 팩토리 패턴 사용 (입력에 따라 다른 객체 생성)
# - 타입에 따라 아예 다른 객체를 생성하는 방식
# - 구조를 더 유연하게 확장 가능 (OCP 만족)
class DisplayString:
    def display(self, data):
        print(f"문자열: {data}")

class DisplayList:
    def display(self, data):
        print(f"리스트: {data}")

class DisplayDict:
    def display(self, data):
        print(f"딕셔너리: {data}")


# 팩토리 패턴의 핵심:
# 객체 생성 new(생성자 호출)를 클래스 외부에 숨기고
# 팩토리 함수 또는 팩토리 클래스를 통해 생성하도록 하는 구조.
def DisplayDataFactory(data):
    if isinstance(data, str):
        return DisplayString()
    elif isinstance(data, list):
        return DisplayList()
    elif isinstance(data, dict):
        return DisplayDict()
    else:
        raise TypeError("지원하지 않는 타입입니다.")

data1 = "hello"
display1 = DisplayDataFactory(data1)
display1.display(data1)  # 문자열: hello

data2 = [1, 2, 3]
display2 = DisplayDataFactory(data2)
display2.display(data2)  # 리스트: [1, 2, 3]

data3 = {"a": 1}
display3 = DisplayDataFactory(data3)
display3.display(data3)  # 딕셔너리: {'a': 1}
