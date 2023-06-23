def get_mode_input():
    while True:
        mode = input("연산모드를 입력하시오: ")
        return is_valid_mode(mode)


def is_valid_mode(mode):
    valid_modes = ['plus', 'minus', 'multiply', 'division']
    if mode not in valid_modes:
        print("유효하지 않은 연산모드입니다. 가능한 모드: ", valid_modes)
    else:
        return mode


def get_number_inputs():
    while True:
        try:
            val1 = int(input("숫자1을 입력하시오: "))
            val2 = int(input("숫자2를 입력하시오: "))
            return val1, val2
        except ValueError:
            print('숫자가 아닌 다른 값이 입력되었습니다. 다시 시도하세요.')


def operation(mode, val1, val2):
    if mode == 'plus':
        result = val1 + val2
    elif mode == 'minus':
        result = val1 - val2
    elif mode == 'multiply':
        result = val1 * val2
    elif mode == 'division':
        if val2 != 0:
            result = val1 / val2
        else:
            print('0으로 나눌 수 없습니다.')
            return

    print('결과:', result)


def run_calculator():
    while True:
        mode = get_mode_input()
        if not mode:
            continue

        print("연산모드:", mode)
        val1, val2 = get_number_inputs()
        operation(mode, val1, val2)

        choice = input("계속해서 다른 연산을 수행하시겠습니까? (y/n): ")
        if choice.lower() != 'y':
            break


run_calculator()
