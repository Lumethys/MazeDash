import random
from collections import deque
from typing import Union, Callable

class MazeGenerator:
  def __init__(self, width: int, height: int, min_distance_between_start_end: Union[int, Callable[[int, int], int]]):
    if width < 4 or height < 4 or width > 50 or height > 50:
      raise ValueError("Maze size must be between 4x4 and 50x50")

    self.width: int = width
    self.height: int = height

    val = min_distance_between_start_end
    self.min_distance_between_start_end: int = val(width, height) if callable(val) else val

    self.retry_count: int = 0
    self.max_retries: int = 3
      
  def generate(self) -> list[list[int]]:
    if self.retry_count >= self.max_retries:
      return self._get_default_maze()
      
    # Initialize grid filled with walls
    maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

    # Directions (up, down, left, right)
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    def carve(x, y):
        maze[y][x] = 0
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1 and maze[ny][nx] == 1:
                # knock down wall between current and neighbor
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    # Start carving from a random odd cell
    start_x = random.randrange(1, self.width - 1, 2)
    start_y = random.randrange(1, self.height - 1, 2)
    carve(start_x, start_y)

    # BFS to ensure solvability & place start/end far apart
    def bfs_distance(start_y: int, start_x: int):
        visited: list[list[bool]] = [[False]*self.width for _ in range(self.height)]
        q: deque[tuple[int, int, int]] = deque([(start_y, start_x, 0)])
        visited[start_y][start_x] = True
        farthest = (start_y, start_x, 0)
        while q:
            y, x, d = q.popleft()
            if d > farthest[2]:
                farthest = (y, x, d)
            for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < self.height and 0 <= nx < self.width and not visited[ny][nx] and maze[ny][nx] == 0:
                    visited[ny][nx] = True
                    q.append((ny, nx, d+1))
        return farthest

    # Pick start as one farthest cell, then end as farthest from start
    sy, sx, _ = bfs_distance(start_y, start_x)
    ey, ex, dist = bfs_distance(sy, sx)

    # Ensure distance is "reasonably far"
    if dist < self.min_distance_between_start_end:
        self.retry_count += 1
        return self.generate()  # retry if too close
    else:
        self.retry_count = 0  # reset retry count on success

    maze[sy][sx] = 2  # start
    maze[ey][ex] = 3  # end

    return maze

  def _get_default_maze(self) -> list[list[int]]:
    return [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]