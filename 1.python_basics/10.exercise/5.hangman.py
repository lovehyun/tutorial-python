import random

def display_hangman(wrong_guesses):
    """
    틀린 횟수에 따라 행맨 그림을 보여주는 함수
    """
    stages = [
        # 0번째: 아무것도 없음
        """
           ------
           |    |
           |
           |
           |
           |
        --------
        """,
        # 1번째: 머리
        """
           ------
           |    |
           |    O
           |
           |
           |
        --------
        """,
        # 2번째: 몸통
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        --------
        """,
        # 3번째: 왼팔
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        --------
        """,
        # 4번째: 오른팔
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        --------
        """,
        # 5번째: 왼다리
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        --------
        """,
        # 6번째: 오른다리 (게임 오버)
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        --------
        """
    ]
    
    return stages[wrong_guesses]

def display_word(word, guessed_letters):
    """
    맞춘 글자는 보여주고, 못 맞춘 글자는 _로 표시
    """
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def get_random_word():
    """
    랜덤한 단어를 선택하는 함수
    """
    words = [
        'python', 'computer', 'programming', 'game', 'coding',
        'algorithm', 'function', 'variable', 'loop', 'condition',
        'string', 'integer', 'boolean', 'list', 'dictionary',
        'class', 'object', 'method', 'module', 'library'
    ]
    return random.choice(words).upper()

def is_word_guessed(word, guessed_letters):
    """
    단어의 모든 글자를 맞췄는지 확인
    """
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True

def hangman_game():
    """
    메인 행맨 게임 함수
    """
    print("🎮 행맨 게임에 오신 것을 환영합니다! 🎮")
    print("컴퓨터가 선택한 단어를 맞춰보세요!")
    print("틀릴 때마다 행맨이 그려집니다. 6번 틀리면 게임 오버!")
    print("-" * 50)
    
    # 게임 초기화
    word = get_random_word()
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = 6
    
    # 게임 루프
    while wrong_guesses < max_wrong and not is_word_guessed(word, guessed_letters):
        # 현재 상태 출력
        print(display_hangman(wrong_guesses))
        print(f"단어: {display_word(word, guessed_letters)}")
        print(f"시도한 글자: {sorted(guessed_letters)}")
        print(f"남은 기회: {max_wrong - wrong_guesses}")
        print("-" * 30)
        
        # 사용자 입력
        guess = input("글자를 입력하세요 (영문 대문자): ").upper()
        
        # 입력 검증
        if len(guess) != 1 or not guess.isalpha():
            print("❌ 영문자 하나만 입력해주세요!")
            continue
        
        if guess in guessed_letters:
            print("❌ 이미 시도한 글자입니다!")
            continue
        
        # 글자 추가
        guessed_letters.add(guess)
        
        # 정답 확인
        if guess in word:
            print(f"✅ 맞습니다! '{guess}'가 단어에 있습니다!")
        else:
            wrong_guesses += 1
            print(f"❌ 틀렸습니다! '{guess}'는 단어에 없습니다.")
        
        print()
    
    # 게임 결과
    print(display_hangman(wrong_guesses))
    print(f"정답: {word}")
    
    if is_word_guessed(word, guessed_letters):
        print("🎉 축하합니다! 단어를 맞췄습니다! 🎉")
    else:
        print("💀 게임 오버! 다음에 다시 도전해보세요! 💀")

def hangman_with_hints():
    """
    힌트 기능이 있는 행맨 게임
    """
    words_with_hints = {
        'PYTHON': '프로그래밍 언어의 이름',
        'COMPUTER': '계산을 하는 전자 기기',
        'PROGRAMMING': '코드를 작성하는 활동',
        'ALGORITHM': '문제를 해결하는 절차',
        'FUNCTION': '특정 작업을 수행하는 코드 블록',
        'VARIABLE': '데이터를 저장하는 공간',
        'LOOP': '반복 실행하는 구조',
        'STRING': '문자들의 연속',
        'INTEGER': '정수를 의미하는 단어',
        'BOOLEAN': '참/거짓 값을 나타내는 자료형'
    }
    
    print("🎮 힌트가 있는 행맨 게임! 🎮")
    print("-" * 50)
    
    word = random.choice(list(words_with_hints.keys()))
    hint = words_with_hints[word]
    
    print(f"💡 힌트: {hint}")
    print()
    
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = 6
    
    while wrong_guesses < max_wrong and not is_word_guessed(word, guessed_letters):
        print(display_hangman(wrong_guesses))
        print(f"단어: {display_word(word, guessed_letters)}")
        print(f"힌트: {hint}")
        print(f"시도한 글자: {sorted(guessed_letters)}")
        print(f"남은 기회: {max_wrong - wrong_guesses}")
        print("-" * 30)
        
        guess = input("글자를 입력하세요 (영문 대문자): ").upper()
        
        if len(guess) != 1 or not guess.isalpha():
            print("❌ 영문자 하나만 입력해주세요!")
            continue
        
        if guess in guessed_letters:
            print("❌ 이미 시도한 글자입니다!")
            continue
        
        guessed_letters.add(guess)
        
        if guess in word:
            print(f"✅ 맞습니다! '{guess}'가 단어에 있습니다!")
        else:
            wrong_guesses += 1
            print(f"❌ 틀렸습니다! '{guess}'는 단어에 없습니다.")
        
        print()
    
    print(display_hangman(wrong_guesses))
    print(f"정답: {word} ({hint})")
    
    if is_word_guessed(word, guessed_letters):
        print("🎉 축하합니다! 단어를 맞췄습니다! 🎉")
    else:
        print("💀 게임 오버! 다음에 다시 도전해보세요! 💀")

def main():
    """
    메인 메뉴
    """
    while True:
        print("\n" + "="*50)
        print("🎮 행맨 게임 메뉴 🎮")
        print("="*50)
        print("1. 일반 게임")
        print("2. 힌트가 있는 게임")
        print("3. 게임 종료")
        print("-"*50)
        
        choice = input("선택하세요 (1-3): ")
        
        if choice == '1':
            hangman_game()
        elif choice == '2':
            hangman_with_hints()
        elif choice == '3':
            print("👋 게임을 종료합니다. 감사합니다!")
            break
        else:
            print("❌ 올바른 번호를 선택해주세요!")
        
        # 다시 플레이할지 묻기
        if choice in ['1', '2']:
            while True:
                play_again = input("\n다시 플레이하시겠습니까? (y/n): ").lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    return
                else:
                    print("y 또는 n을 입력해주세요.")

if __name__ == "__main__":
    main()
