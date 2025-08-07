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


# 테스트
s = Stack()
s.push("A")
s.push("B")
s.push("C")
print(s)  # Stack(bottom → top): ['A', 'B', 'C']

print(s.pop())  # C
print(s.peek())  # B
print(s.size())  # 2
print(s.is_empty())  # False
