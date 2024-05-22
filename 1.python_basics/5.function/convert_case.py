# 1. 대소문자 변환
def convert_case(text):
    converted_text = ""

    for char in text:
        if char.islower():
            converted_text += char.upper()
        elif char.isupper():
            converted_text += char.lower()
        else:
            converted_text += char
    
    return converted_text

text = input("문자열을 입력하세요: ")
converted_text = convert_case(text)

print("대소문자 변환된 문자열:", converted_text)


# 2. 문자열에서 숫자를 제거하는 함수
def remove_numbers(text):
    result = ""
    for char in text:
        if not char.isdigit():
            result += char
    return result

text = input("문자열을 입력하세요: ")
result = remove_numbers(text)

print("숫자가 제거된 문자열:", result)


# 3. 문자열에서 특정 문자를 제거하는 함수
def remove_characters(text, chars_to_remove):
    result = ""
    for char in text:
        if char not in chars_to_remove:
            result += char
    return result

text = input("문자열을 입력하세요: ")
chars_to_remove = input("제거할 문자를 입력하세요: ")
result = remove_characters(text, chars_to_remove)

print("특정 문자가 제거된 문자열:", result)

