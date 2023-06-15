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
