class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, value):
        """값 추가"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        """최솟값 제거 및 반환"""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        # 최솟값 꺼내고 맨 끝값을 루트로 올림
        min_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_value

    def _heapify_up(self, index):
        """위로 올라가며 정렬"""
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        """아래로 내려가며 정렬"""
        length = len(self.heap)
        smallest = index

        while True:
            left = 2 * index + 1
            right = 2 * index + 2

            if left < length and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < length and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def __str__(self):
        return f"MinHeap: {self.heap}"


# 테스트
heap = MinHeap()
for num in [5, 3, 8, 1, 6]:
    heap.push(num)
    print(heap)

print("\n최솟값 순으로 꺼내기:")
while heap.heap:
    print(heap.pop())
