import time
import os
from collections import deque

def bfs_maze(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False]*cols for _ in range(rows)]
    prev = [[None]*cols for _ in range(rows)]
    
    queue = deque([start])
    visited[start[0]][start[1]] = True
    
    # 상하좌우 이동 방향
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while queue:
        x, y = queue.popleft()
        
        if (x, y) == end:
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 0 and not visited[nx][ny]:
                    queue.append((nx, ny))
                    visited[nx][ny] = True
                    prev[nx][ny] = (x, y)
    
    # 경로 추적
    path = []
    current = end
    while current:
        path.append(current)
        current = prev[current[0]][current[1]]
    path.reverse()

    return path

def visualize_maze_with_path(maze, path):
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        if maze_copy[x][y] == 0:
            maze_copy[x][y] = "*"

    print("\n미로 시각화 (경로는 *)\n")
    for row in maze_copy:
        print(" ".join(str(cell) if cell in (0, 1) else cell for cell in row))

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
def print_maze(maze, path, start, end):
    display = [row[:] for row in maze]
    for x, y in path:
        if (x, y) != start and (x, y) != end:
            display[x][y] = "*"
    display[start[0]][start[1]] = "S"
    display[end[0]][end[1]] = "E"

    for row in display:
        print(" ".join(str(cell) for cell in row))

    # print()
    print("\n" + "-" * 20 + "\n")


def bfs_with_animation(maze, start, end, delay=0.5):
    rows, cols = len(maze), len(maze[0])
    visited = [[False]*cols for _ in range(rows)]
    prev = [[None]*cols for _ in range(rows)]

    queue = deque([start])
    visited[start[0]][start[1]] = True

    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while queue:
        x, y = queue.popleft()

        # 화면 초기화 및 경로 출력
        path = []
        cur = (x, y)
        while cur:
            path.append(cur)
            cur = prev[cur[0]][cur[1]]
        path.reverse()

        # clear_screen()
        # 누적 출력
        print_maze(maze, path, start, end)
        time.sleep(delay)

        if (x, y) == end:
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 0 and not visited[nx][ny]:
                    queue.append((nx, ny))
                    visited[nx][ny] = True
                    prev[nx][ny] = (x, y)

    return []


# 테스트
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
end = (4, 4)

path = bfs_maze(maze, start, end)

print("찾은 경로:")
for step in path:
    print(step)

visualize_maze_with_path(maze, path)


print('\n' + '=' * 20 + '\n')

final_path = bfs_with_animation(maze, start, end, delay=0.3)

# 최종 경로 출력
print("\n** 최종 경로 **\n")
print_maze(maze, final_path, start, end)
