def is_leap_year(year):
    # 윤년인지 확인하는 함수
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_days_in_month(year, month):
    # 해당 월의 일수를 반환하는 함수
    if month == 2:  # 2월인 경우
        if is_leap_year(year):
            return 29  # 윤년이면 29일
        else:
            return 28  # 윤년이 아니면 28일
    elif month in [4, 6, 9, 11]:  # 4, 6, 9, 11월인 경우
        return 30  # 30일
    else:
        return 31  # 나머지 월은 31일

def print_calendar(year, month):
    # 달력 헤더 출력
    print(f"{month}월 {year}")
    print("일 월 화 수 목 금 토")

    # 해당 월의 첫 날의 요일을 계산
    first_day = year * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
    # 0: 월요일
    # 1: 화요일
    # 2: 수요일
    # 3: 목요일
    # 4: 금요일
    # 5: 토요일
    # 6: 일요일
    
    for i in range(1, month):
        first_day += get_days_in_month(year, i)

    # 해당 월의 달력 출력
    for i in range(first_day % 7):
        print("  ", end=" ")  # 첫 날 이전의 공백 출력

    for day in range(1, get_days_in_month(year, month) + 1):
        print(f"{day:2d}", end=" ")  # 날짜 출력

        if (first_day + day) % 7 == 0:  # 토요일인 경우 줄바꿈
            print()

    print()  # 마지막 줄바꿈

# 사용자로부터 연도와 월 입력 받기
year = int(input("연도를 입력하세요: "))
month = int(input("월을 입력하세요: "))

# 달력 출력
print_calendar(year, month)
