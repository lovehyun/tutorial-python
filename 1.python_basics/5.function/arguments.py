users = [
    {"name": "Alice", "age": 25, "location": "Seoul", "car": "BMW"},
    {"name": "Bob", "age": 30, "location": "Busan", "car": "Mercedes"},
    {"name": "Charlie", "age": 35, "location": "Daegu", "car": "Audi"},
]

def find_users(criteria):
    result = []
    for user in users:
        if user.get("age") >= criteria.get("min_age", 0) and \
                user.get("location") == criteria.get("location", "") and \
                user.get("car") == criteria.get("car", ""):
            result.append(user)
    return result

# 검색 조건 설정
search_criteria = {
    "min_age": 30,
    "location": "Seoul",
    "car": "Mercedes"
}

# 사용자 검색
matching_users = find_users(search_criteria)

# 검색 결과 출력
print("Matching Users:")
for user in matching_users:
    print(user)
