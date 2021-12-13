import arcade
from typing import Optional

CELL_SIZE = 20
GAME_SIZE = (40, 40)
WIDTH = CELL_SIZE * GAME_SIZE[0]
HEIGHT = CELL_SIZE * GAME_SIZE[1] + 20
TITLE = 'pySnake'
BG_COLOR = arcade.color.WHITE_SMOKE
SNAKE_PART_COLOR = arcade.color.GO_GREEN
SNAKE_HEAD_COLOR = arcade.color.GRAPE
START_LENGTH = 15  # Начальная длина питона
START_DELAY = 1/5  # Начальная задержка таймера


class Timer:
    """Класс таймера. Нужен для того, чтобы регулироват скорост змеи"""
    def __init__(self, start_delay=1/5):
        self.delay = start_delay
        self.current_time = self.delay
    
    def is_update(self, delta_time: float) -> bool:
        self.current_time -= delta_time
        if self.current_time <= 0:
            self.current_time = self.delay
            return True
        return False


class SnakePart:
    """Класс, описывающий часть питона"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = SNAKE_PART_COLOR
    
    def update(self):
        pass

    def draw(self):
        x = self.x * CELL_SIZE + CELL_SIZE/2
        y = self.y * CELL_SIZE + CELL_SIZE/2
        arcade.draw_circle_filled(x, y, CELL_SIZE / 2, self.color)

    def __str__(self):
        return f'x={self.x}  y = {self.y}'


class SnakeHead(SnakePart):
    """Голова питона"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = SNAKE_HEAD_COLOR
        self.move = 'right'  # Может быть 'left', 'right', 'up', 'down'
        self._dx = 0
        self._dy = 0

    def change_move(self, way: str):
        if way not in ('left', 'right', 'up', 'down'):
            raise ValueError(f"Направления движения {way} нет")
        # Проверяем чтобы не было заднего хода
        if ((way == 'left' and self.move == 'right') or
            (way == 'right' and self.move == 'left') or
            (way == 'up' and self.move == 'down') or
            (way == 'down' and self.move == 'up')):
            return
        # Устанавливаем движение через _dx, _dy
        if way == 'left':
            self._dx, self._dy = -1, 0
            self.move = 'left'
        elif way == 'right':
            self._dx, self._dy = 1, 0
            self.move = 'right'
        elif way == 'up':
            self._dx, self._dy = 0, 1
            self.move = 'up'
        elif way == 'down':
            self._dx, self._dy = 0, -1
            self.move = 'down'

    def update(self):
        self.x += self._dx
        self.y += self._dy


class Snake:
    """Класс описывающий всего питона целиком"""
    def __init__(self, x, y):
        self.is_game_over = False
        self.part_list = []
        self.length = START_LENGTH
        self.head = SnakeHead(x, y)
        self.part_list.append(self.head)
        for i in range(1, START_LENGTH):
            snake_part = SnakePart(x-i, y)
            self.part_list.append(snake_part)

    def _make_step(self):
        head = self.part_list[0]
        prev_x = head.x
        prev_y = head.y
        head.update()
        for part in self.part_list[1:]:
            dx = prev_x - part.x
            dy = prev_y - part.y
            prev_x = part.x
            prev_y = part.y
            part.x += dx
            part.y += dy

    def _check_borders(self):
        """Проверяет выход за границы экрана"""
        if self.head.x < 0:
            self.head.x = GAME_SIZE[0]
        elif self.head.x > GAME_SIZE[0] - 1:
            self.head.x = 0
        elif self.head.y < 0:
            self.head.y = GAME_SIZE[1]
        elif self.head.y > GAME_SIZE[1] - 1:
            self.head.y = 0

    def _check_self_byte(self):
        x = self.head.x
        y = self.head.y
        for part in self.part_list[1:]:
            if part.x == x and part.y == y:
                self.is_game_over = True
                break

    def change_move(self, way: str):
        self.head.change_move(way)

    def update(self):
        self._make_step()  # Делаем шаг
        self._check_borders()  # Проверяем выход за границы экрана
        self._check_self_byte()  # Проверяем на самоукус
    
    def draw(self):
        # print(self.part_list[0], self.part_list[1])
        for part in self.part_list[::-1]:
            part.draw()


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, update_rate=1/60)
        self.background_color = BG_COLOR
        self.timer = Timer(start_delay=START_DELAY)
        self.snake: Optional[Snake] = None
        self.status = ''  # Состояние игры (game, game_over)
        self.setup()

    def setup(self):
        self.snake = Snake(10, 10)
        self.snake.change_move('right')
        self.status = 'game'

    def on_key_press(self, symbol, modifiers):
        if self.status == 'game':
            if symbol == arcade.key.UP:
                self.snake.change_move('up')
            elif symbol == arcade.key.DOWN:
                self.snake.change_move('down')
            elif symbol == arcade.key.LEFT:
                self.snake.change_move('left')
            elif symbol == arcade.key.RIGHT:
                self.snake.change_move('right')
    
    def on_update(self, delta_time):
        if self.status == 'game':
            # Дожидаемся таймера
            if self.timer.is_update(delta_time):
                self.snake.update()
                if self.snake.is_game_over:
                    self.status = 'game_over'
        elif self.status == 'game_over':
            pass

    def on_draw(self):
        arcade.start_render()
        if self.status == 'game':
            self.snake.draw()
            text = f'x = {self.snake.head.x}, y = {self.snake.head.y}'
            arcade.draw_text(text, 0, 800, color=arcade.color.BLACK)
        elif self.status == 'game_over':
            self.snake.draw()
            text = 'Игра окончена'
            arcade.draw_text(text, WIDTH // 2, HEIGHT // 2, color=arcade.color.RUBY, font_size=40, anchor_x='center')


if __name__ == '__main__':
    MyGame().run()
