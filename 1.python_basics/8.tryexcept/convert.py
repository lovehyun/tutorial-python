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
