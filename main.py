import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
FPS = 3

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

# Фигуры тетриса
SHAPES = [[[1, 1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]]]


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simple Tetris v 1.0")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_shape = self.new_shape()
        self.next_shape = self.new_shape()
        self.score = 0
        self.game_over = False

    @classmethod
    def new_shape(cls):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return Shape(shape, color)

    def draw_grid(self):
        for y in range(ROWS):
            for x in range(COLUMNS):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for x in range(COLUMNS):
            pygame.draw.line(self.screen, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
        for y in range(ROWS):
            pygame.draw.line(self.screen, WHITE, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))

    def draw_shape(self, shape):
        for y, row in enumerate(shape.shape):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(self.screen, shape.color, ((shape.x + x) * BLOCK_SIZE, (shape.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self, shape):
        for y, row in enumerate(shape.shape):
            for x, block in enumerate(row):
                if block:
                    if x + shape.x < 0 or x + shape.x >= COLUMNS or y + shape.y >= ROWS or self.grid[y + shape.y][x + shape.x]:
                        return True
        return False

    def merge_shape(self, shape):
        for y, row in enumerate(shape.shape):
            for x, block in enumerate(row):
                if block:
                    self.grid[y + shape.y][x + shape.x] = shape.color

    def clear_lines(self):
        lines_cleared = 0
        for y in range(ROWS):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * COLUMNS)
                lines_cleared += 1
        self.score += lines_cleared ** 2

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_shape(self.current_shape)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_shape.x -= 1
                        if self.check_collision(self.current_shape):
                            self.current_shape.x += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_shape.x += 1
                        if self.check_collision(self.current_shape):
                            self.current_shape.x -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_shape.y += 1
                        if self.check_collision(self.current_shape):
                            self.current_shape.y -= 1
                    elif event.key == pygame.K_UP:
                        self.current_shape.rotate()

            self.current_shape.y += 1
            if self.check_collision(self.current_shape):
                self.current_shape.y -= 1
                self.merge_shape(self.current_shape)
                self.clear_lines()
                self.current_shape = self.next_shape
                self.next_shape = self.new_shape()
                if self.check_collision(self.current_shape):
                    self.game_over = True

            pygame.display.flip()
            self.clock.tick(FPS)


class Shape:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLUMNS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self, times=1):
        for _ in range(times):
            self.shape = [list(row) for row in zip(*self.shape[::-1])]


if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()