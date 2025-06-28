users = [
    {"name": "Alice", "age": 25, "location": "Seoul", "car": "BMW"},
    {"name": "Bob", "age": 30, "location": "Busan", "car": "Mercedes"},
    {"name": "Charlie", "age": 35, "location": "Daegu", "car": "Audi"},
]

# 한명만 검색
def find_user(name):
    for user in users:
        if user["name"] == name:
        # if user["name"].lower() == name.lower():
            return user

# 여러명 모두 검색
def find_users(name):
    result = []
    for user in users:
        if user["name"] == name:
            result.append(user)
    return result


# ---------------------
# 미션1. 이름 및 나이로 검색 구현
def find_user2(name=None, age=None):
    for user in users:
        if name is not None and age is not None:
            if user["name"] == name and user["age"] == age:
                return user
        elif name is not None:
            if user["name"] == name:
                return user
        elif age is not None:
            if user["age"] == age:
                return user
    return None

def find_user2_simplified(name=None, age=None):
    for user in users:
        if (name is None or user["name"] == name) and (age is None or user["age"] == age):
            return user

# ---------------------
# 미션2. 다양한 변화하는 검색 조건을 입력 인자에 어떻게 받을 것인가?
# 검색 조건 설정
search_criteria = {
    "min_age": 30,
    "location": "Busan",
    # "car": "Mercedes"
}

def find_users2(condition):
    result = []
    for user in users:
        if user.get("age") >= condition.get("min_age", 0) and \
            user.get("location") == condition.get("location", "") and \
            user.get("car") == condition.get("car", ""):
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
    "name": "Alice",
    "car": "BMW"
}

# 파이썬 스러운 is None 및 get 등을 통해서 구현
def find_users3(search):
    result = []

    for user in users:
        # 미니 미션3-1. min_age는 어떻게 구현?
        # if (search.get("min_age") is None or user.get("age") >= search.get("min_age")) and \

        # 해당 항목이 없으면 무시 (is None) or 있으면 뒤에 조건 비교
        if (search.get("age") is None or user.get("age") == search.get("age")) and \
            (search.get("name") is None or user.get("name") == search.get("name")) and \
            (search.get("location") is None or user.get("location") == search.get("location")) and \
            (search.get("car") is None or user.get("car") == search.get("car")):
                result.append(user)
    return result

# 참고. 레거시 코드 문법을 통해 구현
def find_users4(search):
    result = []
    for user in users:
        if matches_criteria(user, search):
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


# ---------------------
# 미션4. 유닛테스트 만들기
# 미션4-1. 유닛테스트 효율화하기
search_bob1 = { "name": "Bob" } # expect 1
search_bob2 = { "age": 30 } # expect 1
search_bob3 = { "name": "Bob", "age": 30 } # expect 1
search_bob4 = { "name": "Bob", "age": 31 } # expect 0
search_bob5 = { } # expect 3

test_cases = [
    {"case":search_bob1, "expected_result":1},
    {"case":search_bob2, "expected_result":1}, 
    {"case":search_bob3, "expected_result":1}, 
    {"case":search_bob4, "expected_result":0}, 
    {"case":search_bob5, "expected_result":3},
]

def test_find_users():
    final_result = True

    for test_case in test_cases:
        if not len(find_users4(test_case["case"])) == test_case["expected_result"]:
            final_result = False

    if final_result is True:
        print('PASS')
    else:
        print('FAIL')

test_find_users()
