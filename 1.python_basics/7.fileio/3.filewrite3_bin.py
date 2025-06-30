# 바이너리 파일 쓰기

# - struct.calcsize(format) 함수는 주어진 형식(format)의 구조체가 차지하는 바이트 
#   크기를 반환하는 함수입니다. format은 구조체의 필드들을 나타내는 문자열입니다.
# - 여기서 "i"는 4바이트 정수(integer)를 나타내는 형식 문자입니다. "i"는 부호 있는 
#   4바이트 정수를 의미하며, 보통 C 언어의 int 형식과 호환됩니다.
# - 따라서 struct.calcsize("i")는 4를 반환하게 됩니다. 이 값은 해당 형식의 정수가 
#   차지하는 바이트 크기를 의미합니다. 이를 이용하여 이진 파일에서 필요한 바이트 수를 
#   계산하거나, 구조체의 필드 순회 등에 활용할 수 있습니다.

import struct

file_path = "binary_file.bin"
data = [1, 2, 3, 4, 5]

with open(file_path, "wb") as file:
    for number in data:
        binary_data = struct.pack("i", number)
        file.write(binary_data)

print("이진 파일 쓰기 완료:", file_path)
