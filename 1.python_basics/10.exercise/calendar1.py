import calendar

def print_calendar(year, month):
    cal = calendar.monthcalendar(year, month)

    # 달력 헤더 출력
    print(calendar.month_name[month], year)
    print("일 월 화 수 목 금 토")

    # 달력 내용 출력
    for week in cal:
        for day in week:
            if day == 0:
                # 비어있는 날짜는 공백으로 출력
                print("  ", end=" ")
            else:
                print(f"{day:2d}", end=" ")
        print()

# 사용자로부터 연도와 월 입력 받기
year = int(input("연도를 입력하세요: "))
month = int(input("월을 입력하세요: "))

# 달력 출력
print_calendar(year, month)
