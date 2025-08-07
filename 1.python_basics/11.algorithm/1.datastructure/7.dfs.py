# DFS (깊이 우선 탐색) 구현 - 재귀 방식
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()

    if node not in visited:
        print(node, end=' ')
        visited.add(node)
        for neighbor in graph[node]:
            dfs_recursive(graph, neighbor, visited)

# DFS (깊이 우선 탐색) 구현 - 스택 방식 (비재귀)
def dfs_stack(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            print(node, end=' ')
            visited.add(node)
            # 스택은 뒤에 넣은 것이 먼저 나오므로, 순서 유지를 위해 reversed
            stack.extend(reversed(graph[node]))


# 테스트
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

print("\nDFS (재귀):")
dfs_recursive(graph, 'A')  # 출력: A B D E C F

print("\nDFS (스택):")
dfs_stack(graph, 'A')      # 출력: A B D E C F
