# 1. 레거시 코드
def remove_duplicates1(lst):
    unique_lst = []
    for item in lst:
        is_unique = True
        
        for unique_item in unique_lst:
            if item == unique_item:
                is_unique = False
                break

        if is_unique:
            unique_lst.append(item)
    
    return unique_lst


# 2. 파이썬 코드
def remove_duplicates2(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst


# 3. 모던 파이썬 코드
def remove_duplicates2(lst):
    return list(set(lst))


numbers = [1, 2, 3, 4, 3, 2, 1, 5, 6, 7, 6, 5]
unique_numbers = remove_duplicates2(numbers)

print("원본 리스트:", numbers)
print("중복 제거된 리스트:", unique_numbers)
