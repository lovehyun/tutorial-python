class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """큐의 뒤에 항목 추가"""
        self.items.append(item)

    def dequeue(self):
        """큐의 앞에서 항목 제거 및 반환"""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self):
        """큐의 앞 항목 확인 (제거하지 않음)"""
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        """큐가 비었는지 확인"""
        return len(self.items) == 0

    def size(self):
        """큐 크기 반환"""
        return len(self.items)

    def __str__(self):
        return f"Queue(front → back): {self.items}"


# 테스트
q = Queue()

q.enqueue("A")
q.enqueue("B")
q.enqueue("C")
print(q)  # Queue(front → back): ['A', 'B', 'C']

print("dequeue:", q.dequeue())  # A
print(q)  # Queue(front → back): ['B', 'C']

print("peek:", q.peek())  # B
