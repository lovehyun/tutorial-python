users = [
    {"name": "Alice", "age": 25, "location": "Seoul", "car": "BMW"},
    {"name": "Bob", "age": 30, "location": "Busan", "car": "Mercedes"},
    {"name": "Charlie", "age": 35, "location": "Daegu", "car": "Audi"},
]

def find_users(name):
    result = []
    for user in users:
        if user["name"] == name:
            result.append(user)
    return result

# 미션1. 이름 및 나이로 검색 구현

# ---------------------
# 미션2. 다양한 변화하는 검색 조건을 입력 인자에 어떻게 받을 것인가?
# 검색 조건 설정
search_criteria = {
    "min_age": 30,
    "location": "Seoul",
    "car": "Mercedes"
}

def find_users2(criteria):
    result = []
    for user in users:
        if user.get("age") >= criteria.get("min_age", 0) and \
            user.get("location") == criteria.get("location", "") and \
            user.get("car") == criteria.get("car", ""):
            result.append(user)
    return result

# 사용자 검색
matching_users = find_users2(search_criteria)

# 검색 결과 출력
print("Matching Users2:")
for user in matching_users:
    print(user)

# ---------------------
# 미션3. 다양한 변화하는 검색 조건을 입력 인자에 어떻게 받을 것인가?
# 입력 받은 조건에 따라 존재하는 부분만 AND 조건으로 비교하여 결과 반환
search_criteria2 = {
    "name": "Bob",
    "location": "Busan",
}

search_criteria3 = {
    "name": "Bob",
    "car": "Mercedes"
}

def find_users3(criteria):
    result = []
    for user in users:
        if matches_criteria(user, criteria):
            result.append(user)
    return result

def matches_criteria(user, criteria):
    for key, value in criteria.items():
        if key == "age":
            if user.get("age") != value:
                return False
        elif key == "name":
            if user.get("name") != value:
                return False
        elif key == "location":
            if user.get("location") != value:
                return False
        elif key == "car":
            if user.get("car") != value:
                return False
    return True

# 사용자 검색
matching_users = find_users3(search_criteria2)

# 검색 결과 출력
print("Matching Users3:")
for user in matching_users:
    print(user)
