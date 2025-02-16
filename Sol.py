# Импортируем необходимые библиотеки
import pygame
import random

# Инициализация всех модулей Pygame
pygame.init()

# Определяем цвета в формате RGB
WHITE = (255, 255, 255)  # Белый цвет
RED = (255, 0, 0)        # Красный цвет
BLACK = (0, 0, 0)        # Черный цвет
GREEN = (0, 255, 0)      # Зеленый цвет

# Размеры окна
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Размер блока змейки
SNAKE_BLOCK_SIZE = 10

# Устанавливаем скорость змейки (количество кадров в секунду)
SNAKE_SPEED = 15

# Создаем окно игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка на Pygame")

# Настройка шрифтов для отображения текста
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Часы для контроля скорости обновления экрана
clock = pygame.time.Clock()


# Функция для отображения текущего счёта
def display_score(score):
    value = score_font.render(f"Ваш счёт: {score}", True, GREEN)
    screen.blit(value, [0, 0])


# Функция для отображения сообщений (например, проигрыш)
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])


# Функция для отрисовки змейки
def draw_snake(snake_block_size, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, BLACK, [segment[0], segment[1], snake_block_size, snake_block_size])


# Главная функция для управления логикой игры
def game_loop():
    game_over = False
    game_close = False

    # Начальная позиция змейки
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    # Начальные изменения координат
    x1_change = 0
    y1_change = 0

    # Список для хранения сегментов змейки и её начальная длина
    snake_list = []
    length_of_snake = 1

    # Генерация координат еды
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE

    # Пока игрок не проиграл
    while not game_over:

        # Если игрок проиграл, предлагаем начать заново или выйти
        while game_close:
            screen.fill(WHITE)
            display_message("Вы проиграли! Нажмите Q для выхода или C для новой игры", RED)
            pygame.display.update()

            # Слушаем действия пользователя
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Обрабатываем события клавиш для управления
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK_SIZE
                    x1_change = 0

        # Проверяем выход за границы экрана
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        # Обновляем координаты головы змейки
        x1 += x1_change
        y1 += y1_change

        # Заполняем экран белым цветом и рисуем еду
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        # Создаем голову змейки и добавляем в список её сегментов
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        # Если длина списка сегментов змейки превышает её длину, удаляем первый сегмент
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Проверяем столкновение головы с телом
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Рисуем змейку и отображаем текущий счёт
        draw_snake(SNAKE_BLOCK_SIZE, snake_list)
        display_score(length_of_snake - 1)

        # Обновляем экран
        pygame.display.update()

        # Проверяем, съела ли змейка еду
        if x1 == food_x and y1 == food_y:
            # Генерация новой еды
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            # Увеличение длины змейки
            length_of_snake += 1

        # Устанавливаем скорость игры
        clock.tick(SNAKE_SPEED)

    # Завершаем Pygame и выходим из программы
    pygame.quit()
    quit()


# Запуск основного цикла игры
game_loop()