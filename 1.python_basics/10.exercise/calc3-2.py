class Calculator:
    mode = None
    val1 = 0
    val2 = 0

    def get_mode_input(self):
        self.mode = input("연산모드를 입력하시오: ")
        if not self.is_valid_mode():
            self.get_mode_input()

    def is_valid_mode(self):
        valid_modes = ['+', '-', '*', '/']
        if self.mode not in valid_modes:
            print("유효하지 않은 연산모드입니다. 가능한 모드: ", valid_modes)
            return False
        else:
            return True

    def get_number_inputs(self):
        try:
            self.val1 = int(input("숫자1을 입력하시오: "))
            self.val2 = int(input("숫자2를 입력하시오: "))
        except ValueError:
            print('숫자가 아닌 다른 값이 입력되었습니다. 다시 시도하세요.')
            self.get_number_inputs()

    def operation(self):
        if self.mode == '+':
            result = self.val1 + self.val2
        elif self.mode == '-':
            result = self.val1 - self.val2
        elif self.mode == '*':
            result = self.val1 * self.val2
        elif self.mode == '/':
            if self.val2 != 0:
                result = self.val1 / self.val2
            else:
                print('0으로 나눌 수 없습니다.')
                return

        print('결과:', result)

    def run_calculator(self):
        self.get_mode_input()
        print("연산모드:", self.mode)
        self.get_number_inputs()
        self.operation()

        choice = input("계속해서 다른 연산을 수행하시겠습니까? (y/n): ")
        if choice.lower() == 'y':
            self.run_calculator()


calculator = Calculator()
calculator.run_calculator()
