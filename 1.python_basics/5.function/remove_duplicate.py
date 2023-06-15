def remove_duplicates(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst

def remove_duplicates2(lst):
    return list(set(lst))

numbers = [1, 2, 3, 4, 3, 2, 1, 5, 6, 7, 6, 5]
unique_numbers = remove_duplicates(numbers)

print("원본 리스트:", numbers)
print("중복 제거된 리스트:", unique_numbers)
