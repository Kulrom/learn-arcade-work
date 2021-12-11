import arcade

WIDTH = 800
HEIGHT = 800
CELL_SIZE = 20
TITLE = 'pySnake'
BG_COLOR = arcade.color.WHITE_SMOKE
SNAKE_PART_COLOR = arcade.color.GO_GREEN
SNAKE_HEAD_COLOR = arcade.color.GRAPE
START_LENGTH = 6  # Начальная длина питона


class Timer:
    """Класс таймера. Нужен для того, чтобы регулироват скорост змеи"""
    def __init__(self):
        self.delay = 1/5
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
        for i in range(len(self.part_list) - 1):
            t_x = self.part_list[i+1]
            self.part_list[i+1].x = self.part_list[i].x

        head.update()

    
    def draw(self):
        print(self.part_list[0], self.part_list[1])
        for part in self.part_list:
            part.draw()



class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, update_rate=1/60)
        self.background_color = BG_COLOR
        self.timer = Timer()
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