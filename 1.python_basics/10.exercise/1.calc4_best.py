class Calculator:
    def __init__(self):
        # 초기화 → 인스턴스 변수 사용
        self.mode = None
        self.val1 = 0
        self.val2 = 0

    def get_mode_input(self):
        self.mode = input("연산모드를 입력하시오: ")
        if not self.is_valid_mode():
            self.get_mode_input()

    def is_valid_mode(self):
        valid_modes = ['+', '-', '*', '/']
        if self.mode not in valid_modes:
            print("유효하지 않은 연산모드입니다. 가능한 모드: ", valid_modes)
            return False
        return True

    def get_number_inputs(self):
        try:
            self.val1 = int(input("숫자1을 입력하시오: "))
            self.val2 = int(input("숫자2를 입력하시오: "))
        except ValueError:
            print('숫자가 아닌 값이 입력되었습니다. 다시 시도하세요.')
            self.get_number_inputs()

    def operation(self):
        try:
            result = self.calculate(self.mode, self.val1, self.val2)
            print('결과:', result)
        except ZeroDivisionError as e:
            print(f'에러: {e}')

    # 이 함수는 객체와 무관한 유틸 함수라는 걸 명시적으로 보여줄 수 있음.
    # self를 사용하지 않아 객체가 가지고 있는 데이터(속성)를 전혀 참조하지 않음.
    @staticmethod
    def calculate(mode, val1, val2):
        if mode == '+':
            return val1 + val2
        elif mode == '-':
            return val1 - val2
        elif mode == '*':
            return val1 * val2
        elif mode == '/':
            if val2 == 0:
                raise ZeroDivisionError('0으로 나눌 수 없습니다.')  # 예외 발생
            return val1 / val2
        else:
            raise ValueError('알 수 없는 연산모드입니다.')  # 예외 발생

    def run_calculator(self):
        self.get_mode_input()
        print("연산모드:", self.mode)
        self.get_number_inputs()
        self.operation()

        choice = input("계속해서 다른 연산을 수행하시겠습니까? (y/n): ")
        if choice.lower() == 'y':
            self.run_calculator()


if __name__ == "__main__":
    # print(Calculator.calculate('+', 2, 3))  # 이렇게 객체 없이 바로 호출 가능

    calculator = Calculator()
    calculator.run_calculator()

