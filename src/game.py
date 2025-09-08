import pygame
import sys
from snake import Snake
from food import Food
from utils import load_highscore, save_highscore

CELL_SIZE = 20
COLS = 32
ROWS = 24
SCREEN_WIDTH = CELL_SIZE * COLS
SCREEN_HEIGHT = CELL_SIZE * ROWS
FPS_BASE = 8

BG_COLOR = (10, 10, 10)
SNAKE_COLOR = (0, 200, 0)
FOOD_COLOR = (200, 50, 50)
TEXT_COLOR = (255, 255, 255)
PAUSE_COLOR = (255, 220, 0)
GAMEOVER_COLOR = (220, 50, 50)


class Game:
    def __init__(self):
        print("Initializing Game")  # debug to ensure constructor runs
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake+")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 32, bold=True)

        self.best_score = load_highscore()
        self.reset()

    def reset(self):
        self.snake = Snake(COLS, ROWS)
        self.food = Food(self.snake, COLS, ROWS)
        self.score = 0
        self.speed = FPS_BASE
        self.paused = False
        self.game_over = False

    def handle_input(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_UP, pygame.K_w):
                    self.snake.set_direction(0, -1)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.set_direction(0, 1)
                elif ev.key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.set_direction(-1, 0)
                elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.set_direction(1, 0)
                elif ev.key == pygame.K_p:
                    self.paused = not self.paused
                elif ev.key == pygame.K_r and self.game_over:
                    self.reset()
                elif ev.key == pygame.K_q and self.game_over:
                    pygame.quit()
                    sys.exit()

    def update(self):
        if self.paused or self.game_over:
            return
        self.snake.move()

        if self.snake.collides_with_wall() or self.snake.collides_with_self():
            self.game_over = True
            save_highscore(self.score)
            self.best_score = load_highscore()
            return

        # Eating food
        if self.snake.head().x == self.food.position.x and self.snake.head().y == self.food.position.y:
            self.score += 1
            self.snake.grow()
            self.food.randomize(self.snake)
            self.speed = FPS_BASE + (self.score // 3)

    def draw(self):
        self.screen.fill(BG_COLOR)

        # Snake
        for seg in self.snake.body:
            r = pygame.Rect(seg.x * CELL_SIZE, seg.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, SNAKE_COLOR, r)

        # Food
        f = self.food.position
        food_rect = pygame.Rect(f.x * CELL_SIZE, f.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, FOOD_COLOR, food_rect)

        # HUD
        score_surf = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        best_surf = self.font.render(f"Best: {self.best_score}", True, TEXT_COLOR)
        self.screen.blit(score_surf, (6, 6))
        self.screen.blit(best_surf, (6, 30))

        if self.paused:
            p = self.big_font.render("PAUSED (P)", True, PAUSE_COLOR)
            self.screen.blit(p, (SCREEN_WIDTH // 2 - p.get_width() // 2, SCREEN_HEIGHT // 2))

        if self.game_over:
            go = self.big_font.render("GAME OVER", True, GAMEOVER_COLOR)
            instr = self.font.render("R = restart   Q = quit", True, TEXT_COLOR)
            self.screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, SCREEN_HEIGHT // 2 - 36))
            self.screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, SCREEN_HEIGHT // 2 + 8))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(int(self.speed))