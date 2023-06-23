# 미션1. 두개의 숫자와 연산모드를 입력받아 계산기 기능을 수행하시오
# 미션2. 각종 예외처리를 적용하시오

mode = input("연산모드를 입력하시오: ")
val1 = int(input("숫자1을 입력하시오: "))
val2 = int(input("숫자2를 입력하시오: "))

result = None

if mode == 'plus':
    print('덧셈을 시작합니다')
    result = val1 + val2
elif mode == 'minus':
    print('뺄셈을 시작합니다')
    result = val1 + val2
elif mode == 'multiply':
    print('곱셈을 시작합니다')
    result = val1 + val2
elif mode == 'division':
    print('나눗셈을 시작합니다')
    result = val1 + val2
else:
    print('알수 없는 연산모드 입니다.')

print('결과: ', result)
