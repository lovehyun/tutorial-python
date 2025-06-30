# https://docs.python.org/ko/3/library/datetime.html
import datetime

# 모듈명.클래스(객체)명.함수명
# datetime.datetime.now()

# 현재 시간 출력
current_time = datetime.datetime.now()
print("현재 시간:", current_time)
print(datetime.datetime.now().strftime('%Y-%m-%d'))
print(datetime.datetime.now().strftime('%H:%M:%S'))

# 특정 날짜와 시간 생성
specific_time = datetime.datetime(2023, 6, 15, 10, 30, 0)
print("특정 날짜와 시간:", specific_time)

specific_time2 = datetime.datetime(2024, 1, 1)
print("특정 날짜와 시간:", specific_time2)

specific_time3 = datetime.date(2024, 1, 1)
print("특정 날짜와 시간:", specific_time3)


# 또는 from datetime import datetime
# current_time = datetime.now()
# specific_time = datetime(2023, 6, 15, 10, 30, 0)