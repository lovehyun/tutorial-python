# 부모 클래스 Shape (도형의 공통 인터페이스)
class Shape:
    def area(self):
        # 자식 클래스가 반드시 오버라이딩해야 하는 메서드 (여기서는 비워둠)
        pass

# 자식 클래스 Rectangle (사각형)
class Rectangle(Shape):
    def __init__(self, width: int, height: int):
        self.width = width    # 사각형의 가로 길이
        self.height = height  # 사각형의 세로 길이

    def area(self):
        # 사각형의 넓이 계산 (가로 * 세로)
        return self.width * self.height

# 자식 클래스 Circle (원)
class Circle(Shape):
    def __init__(self, radius: int):
        self.radius = radius  # 원의 반지름

    def area(self):
        # 원의 넓이 계산 (πr²)
        return 3.14 * self.radius * self.radius

# Rectangle, Circle 객체를 리스트로 저장 (다형성 활용)
shapes = [Rectangle(4, 5), Circle(3)]

# 모든 도형의 넓이를 일괄적으로 계산 (다형성의 핵심)
for shape in shapes:
    # 다형성: "동일한 코드가 다른 객체에서 다르게 동작하는 것"
    # shape.area() → Rectangle이면 사각형 넓이, Circle이면 원 넓이
    print("Area:", shape.area())
