from random import choice, randint

import pygame as pg

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
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """
    Базовый класс, где хранятся общие атрибуты
    для игровых объектов Apple и Snake
    """

    def __init__(
        self, position: tuple = (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Для отрисовки объекта на экране screen"""
        raise NotImplementedError(f'Ошибка в классе{type(self).__name__}')


class Apple(GameObject):
    """Класс для создания яблока"""

    def __init__(
            self,
            body_color: tuple[int, int, int] = APPLE_COLOR,
            snake_positions: list[tuple[int, int]] | None = None) -> None:
        super().__init__(body_color=body_color)
        self.randomize_position(snake_positions or [])

    def randomize_position(self, snake_positions) -> None:
        """Задаёт случайное положение яблока на экране"""
        while True:
            rand_x = randint(0, GRID_WIDTH - 1)
            rand_y = randint(0, GRID_HEIGHT - 1)
            self.position = (rand_x, rand_y)
            if self.position not in snake_positions:
                break

    def draw(self) -> None:
        """Метод рисует само яблоко"""
        # Переведём сначала в пиксели
        pixel_x = self.position[0] * GRID_SIZE
        pixel_y = self.position[1] * GRID_SIZE
        # Потом передадим эти координаты для отрисовки яблока
        rect = pg.Rect(pixel_x, pixel_y, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс создания змейки"""

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.last: tuple[int, int] | None = None

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

        # Добавляем новое положение головы змейки
        self.positions.insert(0, new_head_position)

        # Если яблоко съедено, то хвост удаляется
        self.last = (
            self.positions.pop() if len(self.positions) > self.length
            else None
        )

    def reset(self) -> None:
        """Метод возвращает змейку на начальную позицию"""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Метод рисует змейку"""
        # Рисуем все сегменты кроме головы
        for position in self.positions[1:]:
            pixel_x = position[0] * GRID_SIZE
            pixel_y = position[1] * GRID_SIZE
            rect = pg.Rect(pixel_x, pixel_y, GRID_SIZE, GRID_SIZE)
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_x = self.positions[0][0] * GRID_SIZE
        head_y = self.positions[0][1] * GRID_SIZE
        head_rect = pg.Rect(head_x, head_y, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_x = self.last[0] * GRID_SIZE
            last_y = self.last[1] * GRID_SIZE
            last_rect = pg.Rect(last_x, last_y, GRID_SIZE, GRID_SIZE)
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запуск игры Змейка"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(APPLE_COLOR, snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
