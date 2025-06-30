# https://docs.python.org/3/library/exceptions.html

# 1. 나눗셈 에러
try:
    result = 10 / 0  # ZeroDivisionError 발생
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")


# 2. 변환 에러
def convert_to_integer(num_str):
    try:
        result = int(num_str)
        return result
    except ValueError:
        print("유효한 숫자로 변환할 수 없습니다.")
        return None

number = convert_to_integer("10")
if number is not None:
    print("숫자 변환 결과:", number)

number = convert_to_integer("A")
if number is not None:
    print("숫자 변환 결과:", number)

