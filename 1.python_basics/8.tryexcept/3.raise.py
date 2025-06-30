# 1. 원하는 조건에 따라 예외 발생
def calculate_square_root(number):
    if number < 0:
        raise ValueError("음수의 제곱근을 계산할 수 없습니다.")
    return number ** 0.5

try:
    result = calculate_square_root(-4)
except ValueError as e:
    print(e)


# 2. 커스텀 예외 발생
class CustomError(Exception):
    pass

# class CustomError(Exception):
#     def __init__(self, message):
#         self.message = message
    
#     def __str__(self):
#         return f'CustomError: {self.message}'
    

def check_value(value):
    if value < 0:
        raise CustomError("음수 값은 허용되지 않습니다.")

try:
    check_value(-5)
except CustomError as e:
    print(e)



# 3. NotImplementedError 예외 발생
class BaseClass:
    def method(self):
        raise NotImplementedError("이 메서드는 서브클래스에서 구현되어야 합니다.")

class SubClass(BaseClass):
    def method(self):
        return "서브클래스에서 구현됨"

try:
    base_instance = BaseClass()
    base_instance.method()
except NotImplementedError as e:
    print(e)

sub_instance = SubClass()
print(sub_instance.method())
