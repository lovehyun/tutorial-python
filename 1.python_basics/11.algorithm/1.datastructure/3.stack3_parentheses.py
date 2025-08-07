class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """스택에 항목 추가"""
        self.items.append(item)

    def pop(self):
        """스택에서 항목 제거 및 반환"""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """스택의 최상단 항목 조회 (제거하지 않음)"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """스택이 비었는지 여부 확인"""
        return len(self.items) == 0

    def size(self):
        """스택의 크기 반환"""
        return len(self.items)

    def __str__(self):
        return f"Stack(bottom → top): {self.items}"

def is_valid_parentheses(expr):
    stack = Stack()
    for char in expr:
        if char == "(":
            stack.push(char)
        elif char == ")":
            if stack.is_empty():
                return False
            stack.pop()
    return stack.is_empty()

def is_valid_parentheses_visual(expr):
    stack = Stack()
    print(f"입력 표현식: {expr}")
    print("-" * 40)

    for i, char in enumerate(expr):
        if char == "(":
            stack.push(char)
            print(f"{i:02d}: '{char}' → push → {stack}")
        elif char == ")":
            if stack.is_empty():
                print(f"{i:02d}: '{char}' → 스택이 비어 있음! 짝이 없음")
                return False
            popped = stack.pop()
            print(f"{i:02d}: '{char}' → pop('{popped}') → {stack}")

    if stack.is_empty():
        print("-" * 40)
        print("괄호 짝이 모두 맞습니다.")
        return True
    else:
        print("-" * 40)
        print(f"아직 스택에 여는 괄호가 남아 있습니다: {stack}")
        return False

def is_valid_parentheses_with_trace(expr):
    stack = Stack()

    for i, char in enumerate(expr):
        if char == "(":
            stack.push(i)  # 괄호 위치를 스택에 저장
        elif char == ")":
            if stack.is_empty():
                print(expr)
                print(" " * i + "^ ← 닫는 괄호가 너무 많습니다!")
                return False
            stack.pop()

    if not stack.is_empty():
        # 남은 열린 괄호 중 첫 번째 위치를 표시
        error_index = stack.pop()
        print(expr)
        print(" " * error_index + "^ ← 여는 괄호가 닫히지 않았습니다!")
        return False

    return True

def is_valid_parentheses_with_trace_visual(expr):
    stack = Stack()
    print(f"입력 표현식: {expr}")
    print("-" * 40)

    for i, char in enumerate(expr):
        if char == "(":
            stack.push(i)
            print(f"{i:02d}: '{char}' → 위치 {i} 저장 → {stack}")
        elif char == ")":
            if stack.is_empty():
                print(f"{i:02d}: '{char}' → 닫는 괄호 '{char}'에 대응되는 여는 괄호 없음!")
                print(expr)
                print(" " * i + "^ ← 닫는 괄호가 너무 많습니다!")
                return False
            popped = stack.pop()
            print(f"{i:02d}: '{char}' → pop 위치 {popped} → {stack}")

    if not stack.is_empty():
        error_index = stack.pop()
        print(f"\n닫히지 않은 여는 괄호가 남아있습니다!")
        print(expr)
        print(" " * error_index + "^ ← 여는 괄호가 닫히지 않았습니다!")
        return False

    print("-" * 40)
    print("괄호 짝이 모두 맞습니다.")
    return True


# 테스트
# print(is_valid_parentheses("(1 + 2) * (3 + (4 - 5))"))  # True
print(is_valid_parentheses_visual("(1 + 2) * (3 + (4 - 5))"))
print()
# print(is_valid_parentheses("((1 + 2)"))  # False
print(is_valid_parentheses_visual("((1 + 2)"))
print()

# print(is_valid_parentheses_with_trace("(1 + 2) * (3 + (4 - 5))"))  # 올바름
print(is_valid_parentheses_with_trace_visual("(1 + 2) * (3 + (4 - 5))"))
print()
# print(is_valid_parentheses_with_trace("((1 + 2)"))                # 여는 괄호 남음
print(is_valid_parentheses_with_trace_visual("((1 + 2)"))
print()
# print(is_valid_parentheses_with_trace("(1 + 2)) + 3"))            # 닫는 괄호 초과
print(is_valid_parentheses_with_trace_visual("(1 + 2)) + 3"))
print()
