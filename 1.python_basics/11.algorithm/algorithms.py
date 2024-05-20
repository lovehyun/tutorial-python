# ------------------------------
# 1. 스택(Stack) 예제
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

# 스택 사용 예제
stack = Stack()
stack.push(10)
stack.push(20)
stack.push(30)
print("Stack Size:", stack.size())
print("Popped Item:", stack.pop())
print("Popped Item:", stack.pop())
print("Is Stack Empty?", stack.is_empty())


# ------------------------------
# 2. 큐(Queue) 예제 - FIFO(First-in, First-out) 구현
from collections import deque

queue = deque()

queue.append(10)
queue.append(20)
queue.append(30)

print("Queue Size:", len(queue))
print("Dequeued Item:", queue.popleft())
print("Dequeued Item:", queue.popleft())
print("Is Queue Empty?", len(queue) == 0)


# ------------------------------
# 3. 연결 리스트(Linked List) 예제
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def print_list(self):
        current = self.head
        while current is not None:
            print(current.data, end=" ")
            current = current.next
        print()

# 연결 리스트 사용 예제
linked_list = LinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)
linked_list.print_list()


# ------------------------------
# 4. 힙(heap) 구현 (Min-heap)
class Heap:
    def __init__(self):
        self.heap = []

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def heapify_up(self, index):
        if index != 0 and self.heap[index] < self.heap[self.parent(index)]:
            parent_index = self.parent(index)
            self.swap(index, parent_index)
            self.heapify_up(parent_index)

    def heapify_down(self, index):
        left = self.left_child(index)
        right = self.right_child(index)
        smallest = index

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self.swap(index, smallest)
            self.heapify_down(smallest)

    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.is_empty():
            min_value = self.heap[0]
            last_index = len(self.heap) - 1
            self.swap(0, last_index)
            self.heap.pop()
            self.heapify_down(0)
            return min_value

    def is_empty(self):
        return len(self.heap) == 0

# Heap 사용 예제
heap = Heap()

# 값 추가
heap.insert(10)
heap.insert(5)
heap.insert(7)
heap.insert(3)
heap.insert(1)

# 최소값 접근
print("최소값:", heap.heap[0])

# 최소값 삭제
min_value = heap.extract_min()
print("최소값 삭제:", min_value)

# 힙 출력
print("Heap:", heap.heap)

# Heap 정렬
sorted_list = []
while not heap.is_empty():
    min_value = heap.extract_min()
    sorted_list.append(min_value)
print("정렬 결과:", sorted_list)


# ------------------------------
# 5. 힙(heap) 라이브러리 활용
import heapq

# 빈 힙 생성
heap = []

# 값 추가
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 7)
heapq.heappush(heap, 3)

# 최소값 접근
print("최소값:", heap[0])

# 최소값 삭제
min_value = heapq.heappop(heap)
print("최소값 삭제:", min_value)

# 힙 정렬
sorted_list = []
while heap:
    sorted_list.append(heapq.heappop(heap))
print("정렬 결과:", sorted_list)

