# print(f"{값:전체자리수.소수점자리수f}")      # 숫자 포맷팅 기본
# print(f"{값:>전체자리수}")                   # 오른쪽 정렬
# print(f"{값:<전체자리수}")                   # 왼쪽 정렬
# print(f"{값:^전체자리수}")                   # 가운데 정렬
# print(f"{값:0전체자리수}")                   # 0으로 자리 채우기
# print(f"{값:,}")                             # 천 단위 콤마 추가

num = 3.141592

# 1. 기본 숫자 포맷팅
print(f"소수점 2자리: {num:.2f}")  # 3.14
print(f"소수점 4자리: {num:.4f}")  # 3.1416

# 2. 전체 자리수 확보 + 소수점 자리수
print(f"전체 8자리, 소수점 2자리: {num:8.2f}")  # '    3.14' (오른쪽 정렬)
print(f"전체 8자리, 소수점 2자리, 0으로 채움: {num:08.2f}")  # '00003.14'

# 3. 정렬 (왼쪽, 오른쪽, 가운데)
text = "Python"
print(f"[{text:<10}]")  # 왼쪽 정렬: [Python    ]
print(f"[{text:>10}]")  # 오른쪽 정렬: [    Python]
print(f"[{text:^10}]")  # 가운데 정렬: [  Python  ]

# 4. 숫자 정렬 + 자리수 + 0 채우기
number = 42
print(f"{number:>5}")   # 오른쪽 정렬: '   42'
print(f"{number:<5}")   # 왼쪽 정렬: '42   '
print(f"{number:^5}")   # 가운데 정렬: ' 42  '
print(f"{number:05}")   # 0으로 채움: '00042'

# 5. 천 단위 콤마
money = 1234567890
print(f"금액: {money:,}원")  # '금액: 1,234,567,890원'

# 6. 문자열 길이 맞추기
name = "Tom"
print(f"[{name:<10}]")  # 왼쪽 정렬: [Tom       ]
print(f"[{name:>10}]")  # 오른쪽 정렬: [       Tom]
print(f"[{name:^10}]")  # 가운데 정렬: [   Tom    ]

# 7. 다양한 데이터 타입 혼합
name = "Alice"
age = 25
height = 162.3456

print(f"이름: {name:<10} 나이: {age:03} 키: {height:6.2f}")
# 결과: 이름: Alice      나이: 025 키: 162.35
