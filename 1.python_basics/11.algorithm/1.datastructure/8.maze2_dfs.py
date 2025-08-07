import time
import sys
sys.setrecursionlimit(10000)

def print_maze(maze, path, start, end):
    display = [row[:] for row in maze]
    for x, y in path:
        if (x, y) != start and (x, y) != end:
            display[x][y] = "*"
    display[start[0]][start[1]] = "S"
    display[end[0]][end[1]] = "E"

    for row in display:
        print(" ".join(str(cell) for cell in row))
    print("\n" + "-" * 20 + "\n")

def dfs_with_animation(maze, x, y, end, visited, path, start, delay=0.3):
    if (x, y) == end:
        path.append((x, y))
        print_maze(maze, path, start, end)
        time.sleep(delay)
        return True

    visited[x][y] = True
    path.append((x, y))

    # 시각화
    print_maze(maze, path, start, end)
    time.sleep(delay)

    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
            if not visited[nx][ny] and maze[nx][ny] == 0:
                if dfs_with_animation(maze, nx, ny, end, visited, path, start, delay):
                    return True

    path.pop()  # 백트래킹
    return False


# 미로
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
end = (4, 4)

visited = [[False]*len(maze[0]) for _ in range(len(maze))]
path = []

dfs_with_animation(maze, start[0], start[1], end, visited, path, start)

# 최종 경로 출력
print("** 최종 경로 (DFS) **\n")
print_maze(maze, path, start, end)
