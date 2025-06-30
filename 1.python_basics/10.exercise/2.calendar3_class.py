class Calendar:
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month

    @staticmethod
    def is_leap_year(year: int) -> bool:
        # 윤년 판별
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def get_days_in_month(year: int, month: int) -> int:
        # 월별 일수 계산
        if month == 2:
            return 29 if Calendar.is_leap_year(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    def get_first_day_of_month(self) -> int:
        # 연도 시작부터 해당 월 첫날까지의 총 일수 계산
        days = self.year * 365 + (self.year - 1) // 4 - (self.year - 1) // 100 + (self.year - 1) // 400

        for m in range(1, self.month):
            days += Calendar.get_days_in_month(self.year, m)

        return days % 7  # 요일 (0: 월요일, ..., 6: 일요일)

    def print_calendar(self):
        print(f"{self.month}월 {self.year}")
        print("일 월 화 수 목 금 토")

        first_day = self.get_first_day_of_month()

        # 첫 주 공백 출력
        for _ in range(first_day):
            print("   ", end="")

        # 날짜 출력
        for day in range(1, Calendar.get_days_in_month(self.year, self.month) + 1):
            print(f"{day:2d}", end=" ")

            if (first_day + day) % 7 == 0:
                print()

        print()  # 마지막 줄바꿈

# 실행 부분
if __name__ == "__main__":
    year = int(input("연도를 입력하세요: "))
    month = int(input("월을 입력하세요: "))

    cal = Calendar(year, month)
    cal.print_calendar()
