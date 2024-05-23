# 1. 대소문자 변환
def convert_case(text):
    converted_text = ""

    # for i in range(len(text)):
        # print(text[i])

    for char in text:
        if char.islower():
            converted_text += char.upper()
        elif char.isupper():
            converted_text += char.lower()
        else:
            converted_text += char
    
    return converted_text


# 1-2. 대소문자 변환 (한줄코드)
def convert_case2(text):
    return ''.join([char.upper() if char.islower() else char.lower() for char in text])


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


# 4. 문자열에서 각 단어의 첫번째 글자를 대문자로 변환하는 함수
def capitalize_words(text):
    result = ""
    words = text.split()
    for word in words:
        result += word.capitalize() + " "
    return result.strip()

text = input("문자열을 입력하세요: ")
result = capitalize_words(text)

print("각 단어의 첫 글자가 대문자로 변환된 문자열:", result)
