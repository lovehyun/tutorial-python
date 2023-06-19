def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

numbers = [3, 7, 2, 9, 1, 4]

# 미션2. 사용자로부터 숫자를 입력받아...
# user_input = input("여러 개의 숫자를 입력하세요 (공백으로 구분): ")
# numbers = [int(num) for num in user_input.split()]

max_number = find_max(numbers)

print("최대값:", max_number)

# 미션3. 모든 구문을 한줄로 구현
# max_value = max([int(x) for x in numbers])
# max_value = max(list(map(lambda x: int(x), numbers)))
