import arcade
import random
from typing import Optional

TITLE = 'pySnake'
CELL_SIZE = 25  # Размер "клетки"
GAME_SIZE = (30, 30)  # Размер игрового поля
INFO_HEIGHT = 20  # Высота строки информации
WIDTH = CELL_SIZE * GAME_SIZE[0]  # Ширина окна
HEIGHT = CELL_SIZE * GAME_SIZE[1] + INFO_HEIGHT  # Высота окна
START_LENGTH = 6  # Начальная длина питона
START_DELAY = 1 / 5  # Начальная задержка таймера в секундах
DELAY_STEP_FACTOR = 0.98  # Множитель, на который уменьшается задержка таймера при каждом съедании кролика
BG_COLOR = arcade.color.WHITE_SMOKE
SNAKE_PART_COLOR = arcade.color.GO_GREEN
SNAKE_HEAD_COLOR = arcade.color.GRAPE
COLOR_INFO_BAR = (204, 222, 131)


class Timer:
    """Класс таймера. Нужен для того, чтобы регулироват скорост змеи"""

    def __init__(self, start_delay: float):
        self.delay = start_delay  # Задержка
        self.current_time = self.delay  # Время оставшееся до "тика"

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
        """Отрисовывает секцию змеи"""
        if (0 <= self.x < GAME_SIZE[0] and  # Если секция внутри игрового поля, то отрисовываем её
                0 <= self.y < GAME_SIZE[1]):
            x = self.x * CELL_SIZE + CELL_SIZE / 2
            y = self.y * CELL_SIZE + CELL_SIZE / 2
            arcade.draw_circle_filled(x, y, CELL_SIZE / 2, self.color)


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

    def __init__(self, x: int, y: int):
        self.is_game_over = False  # Флаг, отвечает за самоукус
        self.is_changed_move = False  # Флаг отвечает за то чтобы за один тик была только одна смена движения
        self.head = SnakeHead(x, y)  # голова змеи
        self._part_list = []
        self.eat_sound = arcade.Sound(':resources:sounds/hurt2.wav')
        self.self_byte_sound = arcade.Sound(':resources:sounds/gameover2.wav')
        self._part_list.append(self.head)

        for i in range(1, START_LENGTH):
            snake_part = SnakePart(x - i, y)
            self._part_list.append(snake_part)

    def _make_step(self):
        head = self._part_list[0]
        prev_x = head.x
        prev_y = head.y
        head.update()
        for part in self._part_list[1:]:
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
        for part in self._part_list[1:]:
            if part.x == x and part.y == y:
                self.is_game_over = True
                self.self_byte_sound.play()
                break

    def is_eat(self, rabbit: 'Rabbit') -> bool:
        """Проверяет был ли съеден кролик"""
        if rabbit.x == self.head.x and rabbit.y == self.head.y:
            self.eat_sound.play(volume=0.3)
            return True
        else:
            return False

    def is_in_snake(self, x, y) -> bool:
        """Проверяет находится ли точка с координатами x, y в теле питона"""
        for part in self._part_list:
            if part.x == x and part.y == y:
                return True
        return False

    def add_part(self):
        """Увеличивает длину змеи"""
        self._part_list.append(SnakePart(-10, -10))

    def change_move(self, way: str):
        if not self.is_changed_move:
            self.head.change_move(way)
            self.is_changed_move = True

    def update(self):
        self._make_step()  # Делаем шаг
        self._check_borders()  # Проверяем выход за границы экрана
        self._check_self_byte()  # Проверяем на самоукус
        self.is_changed_move = False

    def draw(self):
        for part in self._part_list[::-1]:
            part.draw()

    @property
    def length(self) -> int:
        return len(self._part_list)


class Rabbit:
    ANIMATION_SPEED = 8  # Количество тактов на кадр

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cur_texture = 0
        self.sprites = []
        self.texture: Optional[arcade.Sprite] = None
        self._load_textures()

    def _load_textures(self):
        for i in range(1,5):
            sprite = arcade.Sprite(f':resources:images/items/gold_{i}.png')
            sprite.scale = CELL_SIZE / sprite.height
            self.sprites.append(sprite)
        for i in range(3, 1, -1):
            sprite = arcade.Sprite(f':resources:images/items/gold_{i}.png', flipped_horizontally=True)
            sprite.scale = CELL_SIZE / sprite.height
            self.sprites.append(sprite)
        self.texture = self.sprites[0]

    def draw(self):
        self.texture.center_x = self.x * CELL_SIZE + CELL_SIZE / 2
        self.texture.center_y = self.y * CELL_SIZE + CELL_SIZE / 2
        self.texture.draw()

    def update_animation(self, delta_time=1/60):
        self.cur_texture += 1
        if self.cur_texture >= len(self.sprites) * self.ANIMATION_SPEED:
            self.cur_texture = 0
        frame = self.cur_texture // self.ANIMATION_SPEED
        self.texture = self.sprites[frame]


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, update_rate=1 / 60)
        self.background_color = BG_COLOR

        self.timer: Optional[Timer] = None  # создаём таймер
        self.snake: Optional[Snake] = None  # переменная для змеи
        self.rabbit: Optional[Rabbit] = None  # переменная для кролика
        self.score = 0  # Переменная для подсчёта очков
        self.status = ''  # Состояние игры (game, game_over, pause, intro)
        self.font = 'Kenney Blocks'
        self.zastavka = arcade.Sprite('images\zastavka.png')

        self.setup_intro()

    def update_score(self):
        self.score = self.snake.length - START_LENGTH

    def setup_intro(self):
        """Настройки для вступления"""
        self.status = 'intro'

        self.zastavka.scale = 0.7
        self.zastavka.center_x = WIDTH / 2
        self.zastavka.center_y = HEIGHT /2 

    def draw_intro(self):
        self.zastavka.draw()
        text = 'PySnake'
        text_2 = 'press <S> to start'
        arcade.draw_text(text, WIDTH // 2, HEIGHT * 0.8, color=arcade.color.RUBY, font_size=40,
                             anchor_x='center', font_name=self.font)

        arcade.draw_text(text_2, WIDTH // 2, HEIGHT * 0.2, color=arcade.color.RUBY, font_size=20,
                             anchor_x='center', font_name=self.font)
    
    def setup(self):
        """Делает настройки для начала игры"""
        self.snake = Snake(random.randint(START_LENGTH + 10, GAME_SIZE[0] - 10),
                           random.randint(10, GAME_SIZE[1] - 10))
        self.rabbit = Rabbit(0, 0)
        self.change_pos_rabbit()
        self.snake.change_move('right')
        self.status = 'game'
        self.timer = Timer(start_delay=START_DELAY)
        self.update_score()

    def on_key_press(self, symbol, modifiers):
        # Режим игры
        if self.status == 'game':
            if symbol == arcade.key.UP:
                self.snake.change_move('up')
            elif symbol == arcade.key.DOWN:
                self.snake.change_move('down')
            elif symbol == arcade.key.LEFT:
                self.snake.change_move('left')
            elif symbol == arcade.key.RIGHT:
                self.snake.change_move('right')
            elif symbol == arcade.key.SPACE:
                self.status = 'pause'
        # Режим паузы
        elif self.status == 'pause':
            if symbol == arcade.key.SPACE:
                self.status = 'game'
        # Режим Game Over
        elif self.status == 'game_over':
            if symbol == arcade.key.SPACE:
                self.setup()
                self.status = 'game'
        elif self.status == 'intro':
            if symbol == arcade.key.S:
                self.setup()
                self.status = 'game'

    def change_pos_rabbit(self):
        """Меняет позицию кролика"""
        self.rabbit.x = random.randrange(GAME_SIZE[0])
        self.rabbit.y = random.randrange(GAME_SIZE[1])
        if self.snake.is_in_snake(self.rabbit.x, self.rabbit.y):
            self.change_pos_rabbit()

    def on_update(self, delta_time):
        if self.status == 'game':
            # Дожидаемся таймера
            self.rabbit.update_animation()
            if not self.timer.is_update(delta_time):
                return
            self.snake.update()
            if self.snake.is_game_over:
                self.status = 'game_over'
            # Если зайца съели
            if self.snake.is_eat(self.rabbit):
                self.change_pos_rabbit()
                self.snake.add_part()
                self.timer.delay *= DELAY_STEP_FACTOR
            self.update_score()
        elif self.status == 'game_over':
            pass

    def draw_info(self):
        arcade.draw_lrtb_rectangle_filled(0, WIDTH, HEIGHT, HEIGHT - INFO_HEIGHT, color=COLOR_INFO_BAR)
        text = f'Score: {self.score}'
        arcade.draw_text(text, 10, HEIGHT-18, color=arcade.color.BLACK, font_name=self.font)

    def draw_game_frame(self):
        """Отрисовывает игровой кадр"""
        self.snake.draw()
        self.rabbit.draw()
        self.draw_info()

    def on_draw(self):
        arcade.start_render()
        # Режим игры
        if self.status == 'game':
            self.draw_game_frame()
        # Режим паузы
        elif self.status == 'pause':
            self.draw_game_frame()
            text = 'Pause'
            arcade.draw_text(text, WIDTH // 2, HEIGHT // 2, color=arcade.color.RUBY,
                             font_size=30, anchor_x='center', font_name=self.font)
        # режим Game Over
        elif self.status == 'game_over':
            self.draw_game_frame()
            text = 'Game Over'
            text_2 = 'Press <Space> to restart game'
            arcade.draw_text(text, WIDTH // 2, HEIGHT // 2, color=arcade.color.RUBY, font_size=40,
                             anchor_x='center', font_name=self.font)
            arcade.draw_text(text_2, WIDTH // 2, HEIGHT // 2 - 30, color=arcade.color.RUBY, font_size=20,
                             anchor_x='center', font_name=self.font)
        
        elif self.status == 'intro':
            self.draw_intro()
            


if __name__ == '__main__':
    MyGame().run()
