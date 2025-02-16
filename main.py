# Импортируем необходимые библиотеки
import sys

import pygame
from random import randrange

# Инициализация всех модулей Pygame
pygame.init()

# Определяем цвета
RED: tuple[int, int, int] = (255, 0, 0)  # Красный цвет
GREEN: tuple[int, int, int] = (0, 255, 0)  # Зелёный цвет
BLUE: tuple[int, int, int] = (0, 0, 255)  # Синий  цвет
BLACK: tuple[int, int, int] = (0, 0, 0)  # Черный цвет
WHITE: tuple[int, int, int] = (255, 255, 255)  # Белый цвет

# Размеры окна
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600

# Размер блока змейки
SNAKE_BLOCK_SIZE: int = 10

# Устанавливаем скорость змейки (количество кадров в секунду)
SNAKE_SPEED: int = 15

# Создаем окно игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Простая змейка на Pygame')

# Настройка шрифтов для отображения текста
font_style = pygame.font.SysFont('fonts/bahnschrift.ttf', 35)
score_font = pygame.font.Font('fonts/trebucbd.ttf', 25)

# Часы для контроля скорости обновления экрана
clock = pygame.time.Clock()


# Функция для отображения текущего счёта
def display_score(score):
    value = score_font.render(f'Ваш счёт: {score}', True, BLUE)
    screen.blit(value, [0, 0])


# Функция для отображения сообщений (например, проигрыш)
def display_message(msg, color):
    message = font_style.render(msg, True, color)
    screen.blit(message, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])


# Функция для отрисовки змейки
def draw_snake(snake_block_size, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, BLACK, [segment[0], segment[1], snake_block_size, snake_block_size])


# Главная функция для управления логикой игры
def game_loop():
    game_over: bool = False
    game_close: bool = False

    # Начальная позиция змейки
    x1: int = int(SCREEN_WIDTH / 2)
    y1: int = int(SCREEN_HEIGHT / 2)

    # Начальные изменения координат
    x1_change: int = 0
    y1_change: int = 0

    # Список для хранения сегментов змейки и её начальная длина
    snake_list: list[list[int]] = []
    length_of_snake: int = 1

    # Генерация координат еды
    food_x: int = round(randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    food_y: int = round(randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE

    # Пока игрок не проиграл
    while not game_over:

        # Если игрок проиграл, предлагаем начать заново или выйти
        while game_close:
            screen.fill(WHITE)

            loose_text = font_style.render('Вы проиграли!', True, RED)
            guide_text = font_style.render('Нажмите Q для выхода или C для новой игры', True, RED)

            loose_rect = loose_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
            guide_rect = guide_text.get_rect(center=(SCREEN_WIDTH // 2, 270))

            screen.blit(loose_text, loose_rect)
            screen.blit(guide_text, guide_rect)

            pygame.display.update()

            # Слушаем действия пользователя
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over: bool = True
                        game_close: bool = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Обрабатываем события клавиш для управления
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over: bool = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change: int = -SNAKE_BLOCK_SIZE
                    y1_change: int = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change: int = SNAKE_BLOCK_SIZE
                    y1_change: int = 0
                elif event.key == pygame.K_UP:
                    y1_change: int = -SNAKE_BLOCK_SIZE
                    x1_change: int = 0
                elif event.key == pygame.K_DOWN:
                    y1_change: int = SNAKE_BLOCK_SIZE
                    x1_change: int = 0

        # Проверяем выход за границы экрана
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close: bool = True

        # Обновляем координаты головы змейки
        x1: int
        y1: int

        x1 += x1_change
        y1 += y1_change

        # Заполняем экран белым цветом и рисуем еду
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        # Создаем голову змейки и добавляем в список её сегментов
        snake_head: list[int] = [x1, y1]
        snake_list.append(snake_head)

        # Если длина списка сегментов змейки превышает её длину, удаляем первый сегмент
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Проверяем столкновение головы с телом
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close: bool = True

        # Рисуем змейку и отображаем текущий счёт
        draw_snake(SNAKE_BLOCK_SIZE, snake_list)
        display_score(length_of_snake - 1)

        # Обновляем экран
        pygame.display.update()

        # Проверяем, съела ли змейка еду
        if x1 == food_x and y1 == food_y:
            # Генерация новой еды
            food_x: int = round(
                randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            food_y: int = round(
                randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            # Увеличение длины змейки
            length_of_snake += 1

        # Устанавливаем скорость игры
        clock.tick(SNAKE_SPEED)

    # Завершаем Pygame и выходим из программы
    pygame.quit()
    sys.exit(0)


# Запуск основного цикла игры
game_loop()