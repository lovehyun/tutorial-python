import heapq

min_heap = []

# 값 추가
heapq.heappush(min_heap, 4)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 7)

print(min_heap)  # 내부 구조 확인: [1, 4, 7]

# 최솟값 꺼내기
print(heapq.heappop(min_heap))  # 1
print(heapq.heappop(min_heap))  # 4
