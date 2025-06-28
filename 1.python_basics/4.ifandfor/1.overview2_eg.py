# ===================================================================
# 조건문 실전 연습: 계산기 & 가위바위보 게임
# ===================================================================

print("=" * 60)
print("조건문 실전 연습 프로그램")
print("1. 계산기")
print("2. 가위바위보 게임")
print("=" * 60)

# ===================================================================
# 1. 계산기 만들기
# ===================================================================

print("\n" + "=" * 30)
print("🧮 간단한 계산기")
print("=" * 30)

# 사용자 입력 (실제 실행 시에는 input() 사용)
# 예제에서는 미리 값을 설정
print("두 숫자와 연산자를 입력하세요.")

# 실제 사용 시:
# num1 = float(input("첫 번째 숫자: "))
# operator = input("연산자 (+, -, *, /): ")
# num2 = float(input("두 번째 숫자: "))

# 예제용 값들
num1 = 15.5
operator = "+"
num2 = 4.2

print(f"입력: {num1} {operator} {num2}")

# 계산 수행
if operator == "+":
    result = num1 + num2
    operation_name = "덧셈"
elif operator == "-":
    result = num1 - num2
    operation_name = "뺄셈"
elif operator == "*":
    result = num1 * num2
    operation_name = "곱셈"
elif operator == "/":
    if num2 != 0:  # 0으로 나누기 방지
        result = num1 / num2
        operation_name = "나눗셈"
    else:
        result = None
        operation_name = "오류"
        print("❌ 0으로 나눌 수 없습니다!")
else:
    result = None
    operation_name = "오류"
    print("❌ 올바르지 않은 연산자입니다. (+, -, *, / 만 사용 가능)")

# 결과 출력
if result is not None:
    print(f"✅ {operation_name} 결과: {num1} {operator} {num2} = {result}")
    
    # 추가 정보 제공
    if operator == "/" and result.is_integer():
        print(f"💡 결과가 정수입니다: {int(result)}")
    elif operator == "*" and (num1.is_integer() and num2.is_integer()):
        print("💡 정수끼리의 곱셈입니다.")

print("\n" + "-" * 40)
print("🔢 고급 계산기 (여러 연산자 지원)")
print("-" * 40)

# 고급 계산기 예제들
test_cases = [
    (10, "+", 5),
    (20, "-", 8),
    (6, "*", 7),
    (15, "/", 3),
    (10, "/", 0),  # 0으로 나누기 테스트
    (8, "%", 3),   # 나머지 연산
    (2, "**", 3),  # 거듭제곱
    (5, "@", 3),   # 잘못된 연산자
]

for num1, op, num2 in test_cases:
    print(f"\n계산: {num1} {op} {num2}")
    
    if op == "+":
        result = num1 + num2
        print(f"결과: {result}")
    elif op == "-":
        result = num1 - num2
        print(f"결과: {result}")
    elif op == "*":
        result = num1 * num2
        print(f"결과: {result}")
    elif op == "/":
        if num2 != 0:
            result = num1 / num2
            print(f"결과: {result}")
        else:
            print("❌ 오류: 0으로 나눌 수 없습니다!")
    elif op == "%":
        if num2 != 0:
            result = num1 % num2
            print(f"나머지: {result}")
        else:
            print("❌ 오류: 0으로 나눌 수 없습니다!")
    elif op == "**":
        result = num1 ** num2
        print(f"거듭제곱 결과: {result}")
    else:
        print(f"❌ 오류: '{op}'는 지원하지 않는 연산자입니다.")
        print("지원하는 연산자: +, -, *, /, %, **")

# ===================================================================
# 2. 가위바위보 게임
# ===================================================================

print("\n\n" + "=" * 30)
print("✂️📄🗿 가위바위보 게임")
print("=" * 30)

import random

# 게임 규칙 설명
print("게임 규칙:")
print("1 = 가위 ✂️")
print("2 = 바위 🗿") 
print("3 = 보 📄")
print("가위는 보를 이기고, 바위는 가위를 이기고, 보는 바위를 이깁니다.")

# 실제 사용 시:
# user_choice = int(input("\n선택하세요 (1=가위, 2=바위, 3=보): "))

# 예제용 게임들
game_scenarios = [
    (1, "가위 선택"),
    (2, "바위 선택"), 
    (3, "보 선택"),
    (4, "잘못된 입력"),
]

for user_choice, scenario_name in game_scenarios:
    print(f"\n🎮 게임 시나리오: {scenario_name}")
    print("-" * 25)
    
    # 사용자 입력 검증
    if user_choice < 1 or user_choice > 3:
        print("❌ 잘못된 입력입니다. 1, 2, 3 중에서 선택해주세요.")
        continue
    
    # 컴퓨터 선택 (랜덤)
    computer_choice = random.randint(1, 3)
    
    # 선택을 문자열로 변환
    choices = {1: "가위 ✂️", 2: "바위 🗿", 3: "보 📄"}
    
    user_choice_str = choices[user_choice]
    computer_choice_str = choices[computer_choice]
    
    print(f"당신의 선택: {user_choice_str}")
    print(f"컴퓨터 선택: {computer_choice_str}")
    
    # 승부 판정
    if user_choice == computer_choice:
        result = "무승부! 🤝"
        emoji = "😐"
    elif (user_choice == 1 and computer_choice == 3) or \
         (user_choice == 2 and computer_choice == 1) or \
         (user_choice == 3 and computer_choice == 2):
        result = "당신이 이겼습니다! 🎉"
        emoji = "😊"
    else:
        result = "컴퓨터가 이겼습니다! 😢"
        emoji = "😞"
    
    print(f"\n🏆 결과: {result} {emoji}")
    
    # 이긴 이유 설명
    if user_choice != computer_choice:
        if (user_choice == 1 and computer_choice == 3):
            print("💡 가위가 보를 자릅니다!")
        elif (user_choice == 2 and computer_choice == 1):
            print("💡 바위가 가위를 부숩니다!")
        elif (user_choice == 3 and computer_choice == 2):
            print("💡 보가 바위를 감쌉니다!")
        elif (computer_choice == 1 and user_choice == 3):
            print("💡 가위가 보를 자릅니다!")
        elif (computer_choice == 2 and user_choice == 1):
            print("💡 바위가 가위를 부숩니다!")
        elif (computer_choice == 3 and user_choice == 2):
            print("💡 보가 바위를 감쌉니다!")

print("\n" + "-" * 40)
print("🏆 연속 가위바위보 게임 (5라운드)")
print("-" * 40)

# 연속 게임 시뮬레이션
user_wins = 0
computer_wins = 0
ties = 0

# 5라운드 게임 예제
rounds = [2, 1, 3, 2, 1]  # 미리 정해진 사용자 선택들

for round_num in range(1, 6):
    print(f"\n🎯 라운드 {round_num}")
    print("-" * 15)
    
    user_choice = rounds[round_num - 1]
    computer_choice = random.randint(1, 3)
    
    choices = {1: "가위 ✂️", 2: "바위 🗿", 3: "보 📄"}
    
    print(f"당신: {choices[user_choice]}")
    print(f"컴퓨터: {choices[computer_choice]}")
    
    # 승부 판정
    if user_choice == computer_choice:
        print("무승부!")
        ties += 1
    elif (user_choice == 1 and computer_choice == 3) or \
         (user_choice == 2 and computer_choice == 1) or \
         (user_choice == 3 and computer_choice == 2):
        print("당신 승리! 🎉")
        user_wins += 1
    else:
        print("컴퓨터 승리! 🤖")
        computer_wins += 1

# 최종 결과
print("\n" + "=" * 30)
print("🏆 최종 결과")
print("=" * 30)
print(f"당신: {user_wins}승")
print(f"컴퓨터: {computer_wins}승")
print(f"무승부: {ties}회")

if user_wins > computer_wins:
    final_result = "🎉 축하합니다! 당신이 최종 승리했습니다!"
elif computer_wins > user_wins:
    final_result = "😢 아쉽게도 컴퓨터가 이겼습니다. 다음에 다시 도전하세요!"
else:
    final_result = "🤝 무승부입니다! 실력이 비슷하네요!"

print(f"\n{final_result}")

# ===================================================================
# 학습 포인트 정리
# ===================================================================

print("\n📚 학습 포인트:")
print("-" * 20)
print("1. 계산기: 다양한 연산자 처리와 예외 상황 처리")
print("2. 가위바위보: 복잡한 조건 비교와 게임 로직 구현")
print("3. 입력 검증: 잘못된 입력에 대한 오류 처리")
print("4. 조건문 중첩: 복잡한 판정 로직 구현")
print("5. 실생활 응용: 조건문을 활용한 실용적인 프로그램 제작")

print("\n💡 연습 과제:")
print("-" * 15)
print("1. 계산기에 더 많은 연산 추가 (제곱근, 팩토리얼 등)")
print("2. 가위바위보에 새로운 규칙 추가")
print("3. 두 프로그램을 합쳐서 메뉴 시스템 만들기")
print("4. 점수 누적 시스템 추가")
print("5. 게임 히스토리 기능 추가")
