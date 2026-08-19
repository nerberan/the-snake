from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """
    Базовый класс, где хранятся общие атрибуты
    для игровых объектов Apple и Snake
    """

    def __init__(
        self, position: tuple = (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        body_color: tuple[int, int, int] = (0, 0, 0)
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Для отрисовки объекта на экране screen"""
        pass


class Apple(GameObject):
    """Класс для создания яблока"""

    def __init__(self) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Задаёт случайное положение яблока на экране"""
        rand_x = randint(0, GRID_WIDTH - 1)
        rand_y = randint(0, GRID_HEIGHT - 1)
        self.position = (rand_x, rand_y)

    def draw(self) -> None:
        """Метод рисует само яблоко"""
        # Переведём сначала в пиксели
        pixel_x = self.position[0] * GRID_SIZE
        pixel_y = self.position[1] * GRID_SIZE
        # Потом передадим эти координаты для отрисовки яблока
        rect = pygame.Rect(pixel_x, pixel_y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс создания змейки"""

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self) -> tuple:
        """Метод возвращает первый элемент (голова змейки) из списка"""
        return self.positions[0]

    def move(self) -> None:
        """Метод описывает движение змейки"""
        # Получаем координаты головы змейки в клетках (16, 12)
        head_x, head_y = self.get_head_position()
        # Получаем направление движения, по определению в право (1, 0)
        dir_x, dir_y = self.direction
        # Определяем новое положение головы змейки (16+1)%32=17
        new_head_position = ((head_x + dir_x) % GRID_WIDTH,
                             (head_y + dir_y) % GRID_HEIGHT)

        # Проверяем столкновение с телом змейки
        if new_head_position in self.positions:
            self.reset()
            return
        # Добавляем новое положение головы змейки
        self.positions.insert(0, new_head_position)

        # Если яблоко не съедено - хвост удаляется
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self) -> None:
        """Метод возвращает змейку на начальную позицию"""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        start_position = (start_x, start_y)
        self.position = start_position
        self.positions = [start_position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Метод рисует змейку"""
        # Рисуем все сегменты кроме головы
        for position in self.positions[:-1]:
            pixel_x = position[0] * GRID_SIZE
            pixel_y = position[1] * GRID_SIZE
            rect = pygame.Rect(pixel_x, pixel_y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_x = self.positions[0][0] * GRID_SIZE
        head_y = self.positions[0][1] * GRID_SIZE
        head_rect = pygame.Rect(head_x, head_y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_x = self.last[0] * GRID_SIZE
            last_y = self.last[1] * GRID_SIZE
            last_rect = pygame.Rect(last_x, last_y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    ...

    # while True:
    #     clock.tick(SPEED)

        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
