def find_max(numbers):
    max_num = numbers[0]

    for num in numbers:
        if num > max_num:
            max_num = num
    
    return max_num


numbers = [3, 7, 2, 9, 1, 4, 5, 8, 6]

max_number = find_max(numbers)
# max_number = max(numbers) # 내장 함수

# 역순 정렬
# numbers.sort(reverse=True)
# 첫 번째 값이 가장 큰 값
# largest = numbers[0]


print("최대값:", max_number)

# 미션2. 사용자로부터 숫자를 입력받아...
# user_input = input("여러 개의 숫자를 입력하세요 (공백으로 구분): ")
# numbers = [int(num) for num in user_input.split()]

# 미션3. 모든 구문을 한줄로 구현
# max_value = max([int(x) for x in numbers])
# max_value = max(list(map(lambda x: int(x), numbers)))
