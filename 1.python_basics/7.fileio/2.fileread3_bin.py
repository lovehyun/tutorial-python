# 이진 파일 읽기

# 이진 파일의 경우 pack() 함수로 데이터를 이진 형식으로 변환하고, 
# unpack() 함수로 이진 데이터를 원래 형식으로 변환하여 읽습니다.

import struct

file_path = "binary_file.bin"

with open(file_path, "rb") as file:
    binary_data = file.read()

data = []
data_size = len(binary_data) // struct.calcsize("i")
for i in range(data_size):
    offset = i * struct.calcsize("i")
    number = struct.unpack("i", binary_data[offset:offset+struct.calcsize("i")])[0]
    data.append(number)

print("이진 파일 읽기 완료:", file_path)
print("데이터:", data)
