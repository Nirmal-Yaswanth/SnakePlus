from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    x: int
    y: int

class Snake:
    def __init__(self, cols, rows):   # ✅ must accept cols, rows
        mid_x = cols // 2
        mid_y = rows // 2
        self.body: List[Point] = [
            Point(mid_x, mid_y),
            Point(mid_x - 1, mid_y),
            Point(mid_x - 2, mid_y),
        ]
        self.direction = Point(1, 0)
        self._grow = 0
        self.cols = cols
        self.rows = rows

    def head(self) -> Point:
        return self.body[0]

    def set_direction(self, dx, dy):
        # Prevent reversing directly
        if dx == -self.direction.x and dy == -self.direction.y:
            return
        self.direction = Point(dx, dy)

    def move(self):
        new_head = Point(self.head().x + self.direction.x, self.head().y + self.direction.y)
        self.body.insert(0, new_head)
        if self._grow > 0:
            self._grow -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self._grow += amount

    def collides_with_self(self):
        h = self.head()
        return any(p.x == h.x and p.y == h.y for p in self.body[1:])

    def collides_with_wall(self):
        h = self.head()
        return not (0 <= h.x < self.cols and 0 <= h.y < self.rows)