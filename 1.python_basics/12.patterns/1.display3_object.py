# 만약 타입이 개별 클래스 객체들이라면,
# - 타입이 많아도 깔끔하게 확장 가능
# - 딕셔너리 매핑은 객체 지향 설계에서도 매우 유용
class Dog:
    pass

class Cat:
    pass

class Human:
    pass

class DisplayData:
    def __init__(self, data):
        self.handlers = {
            Dog: self.display_dog,
            Cat: self.display_cat,
            Human: self.display_human
        }
        handler = self.handlers.get(type(data), self.unsupported_type)
        handler(data)

    def display_dog(self, data):
        print(f"강아지 객체 처리: {data}")

    def display_cat(self, data):
        print(f"고양이 객체 처리: {data}")

    def display_human(self, data):
        print(f"사람 객체 처리: {data}")

    def unsupported_type(self, data):
        print("지원하지 않는 객체 타입입니다.")

DisplayData(Dog())    # 강아지 객체 처리
DisplayData(Cat())    # 고양이 객체 처리
DisplayData(Human())  # 사람 객체 처리
DisplayData(123)      # 지원하지 않는 객체 타입입니다.

# 덕(Duck) 타이핑



# Class Registry 패턴
#---------------------------------------------------
# DisplayData2는 절대 수정하지 않아도 됨 (OCP 완벽 만족)
# - 새로운 타입은 클래스 + 핸들러만 추가하면 끝
# - 매우 깔끔하고 파이써닉함
# - 확장성, 유지보수 최강
class DisplayData2:
    handlers = {}

    @classmethod
    def register(cls, obj_type):
        def decorator(func):
            cls.handlers[obj_type] = func
            return func
        return decorator

    def __init__(self, data):
        handler = self.handlers.get(type(data), self.unsupported_type)
        handler(self, data)

    def unsupported_type(self, data):
        print("지원하지 않는 객체 타입입니다.")


# Dog 등록
@DisplayData2.register(Dog)
def display_dog(self, data):
    print(f"강아지 객체 처리: {data}")

# Cat 등록
@DisplayData2.register(Cat)
def display_cat(self, data):
    print(f"고양이 객체 처리: {data}")

# Human 등록
@DisplayData2.register(Human)
def display_human(self, data):
    print(f"사람 객체 처리: {data}")


DisplayData2(Dog())    # 강아지 객체 처리
DisplayData2(Cat())    # 고양이 객체 처리
DisplayData2(Human())  # 사람 객체 처리
DisplayData2(123)      # 지원하지 않는 객체 타입입니다.
