import random
from snake import Point

class Food:
    def __init__(self, snake, cols, rows):
        self.cols = cols
        self.rows = rows
        self.position = Point(0, 0)
        self.randomize(snake)

    def randomize(self, snake):
        while True:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if all(p.x != x or p.y != y for p in snake.body):
                self.position = Point(x, y)
                break