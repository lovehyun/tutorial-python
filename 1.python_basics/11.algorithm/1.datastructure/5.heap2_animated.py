import math
import time

class AnimatedMinHeap:
    def __init__(self):
        self.heap = []

    def push(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
        self._visualize(f"push({value})")
        time.sleep(1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            val = self.heap.pop()
            self._visualize(f"pop() → {val}")
            time.sleep(1)
            return val
        min_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        self._visualize(f"pop() → {min_value}")
        time.sleep(1)
        return min_value

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        size = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def _visualize(self, operation=""):
        if not self.heap:
            print(f"[ {operation} 실행 후 힙 상태 ]")
            print("(empty)\n")
            return

        depth = math.floor(math.log2(len(self.heap))) + 1
        width = 2 ** depth * 2  # 전체 너비 설정
        lines = [""] * depth

        for i, value in enumerate(self.heap):
            level = math.floor(math.log2(i + 1))
            index_on_level = i - (2 ** level - 1)
            spacing = width // (2 ** (level + 1))
            if index_on_level == 0:
                lines[level] += " " * spacing
            else:
                lines[level] += " " * (spacing * 2)
            lines[level] += f"{value}"

        print(f"[ {operation} 실행 후 힙 상태 ]")
        for line in lines:
            print(line)
        print()

# 테스트
heap = AnimatedMinHeap()
for val in [7, 2, 9, 4, 1, 5, 3]:
    heap.push(val)

time.sleep(2)

while heap.heap:
    heap.pop()
