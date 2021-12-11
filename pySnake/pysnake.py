import arcade

CELL_SIZE = 20
GAME_SIZE = (40, 40)
WIDTH = CELL_SIZE * GAME_SIZE[0]
HEIGHT = CELL_SIZE * GAME_SIZE[1] + 20
TITLE = 'pySnake'
BG_COLOR = arcade.color.WHITE_SMOKE
SNAKE_PART_COLOR = arcade.color.GO_GREEN
SNAKE_HEAD_COLOR = arcade.color.GRAPE
START_LENGTH = 6  # Начальная длина питона
START_DELAY = 1/5 # Начальная задержка таймера


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
        arcade.draw_circle_filled(x, y, CELL_SIZE / 2 , self.color)

    def __str__(self):
        return f'x={self.x}  y = {self.y}'


class SnakeHead(SnakePart):
    """Голова питона"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = SNAKE_HEAD_COLOR
        self.dx = 1
        self.dy = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy


class Snake:
    """Класс описывающий всего питона целиком"""
    def __init__(self, x, y):
        self.part_list = []
        self.length = START_LENGTH
        self.part_list.append(SnakeHead(x, y))
        for i in range(1, START_LENGTH):
            snake_part = SnakePart(x-i , y)
            self.part_list.append(snake_part)

    def update(self):
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

    
    def draw(self):
        # print(self.part_list[0], self.part_list[1])
        for part in self.part_list:
            part.draw()



class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, update_rate=1/60)
        self.background_color = BG_COLOR
        self.timer = Timer(start_delay=START_DELAY)
        self.setup()

    def setup(self):
        self.snake = Snake(10, 10)
    
    def on_update(self, delta_time):
        if self.timer.is_update(delta_time):
            self.snake.update()

    def on_draw(self):
        arcade.start_render()
        self.snake.draw()


if __name__ == '__main__':
    MyGame().run()