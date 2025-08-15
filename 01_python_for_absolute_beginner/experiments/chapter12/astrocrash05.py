# Прерванный полет-5
# Теперь ракеты стреляют с задержкой

import math, random
from superwires import games

games.init(screen_width=640, screen_height=480, fps=50)


class Asteroid(games.Sprite):
    """ Астероид, прямолинейно движущийся по экрану. """

    # Размеры астероидов
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    # Изображения для разных размеров астероидов
    images = {SMALL: games.load_image("asteroid_small.bmp"),
              MEDIUM: games.load_image("asteroid_med.bmp"),
              LARGE: games.load_image("asteroid_big.bmp")}

    # Скорость астероидов
    SPEED = 2

    def __init__(self, x, y, size):
        """ Инициализирует спрайт с изображением астероида. """
        # Инициализация астероида с изображением, скоростью и позицией
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],
            x=x, y=y,
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,
            dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)

        # Сохраняем размер астероида для использования в будущем
        self.size = size

    def update(self):
        """ Заставляет астероид обогнуть экран. """

        # Если астероид выходит за нижнюю границу экрана, появляется сверху
        if self.top > games.screen.height:
            self.bottom = 0

        # Если астероид выходит за верхнюю границу экрана, появляется снизу
        if self.bottom < 0:
            self.top = games.screen.height

        # Если астероид выходит за правую границу экрана, появляется слева
        if self.left > games.screen.width:
            self.right = 0

        # Если астероид выходит за левую границу экрана, появляется справа
        if self.right < 0:
            self.left = games.screen.width


class Ship(games.Sprite):
    """ Корабль игрока. """

    # Изображение и звук для корабля
    image = games.load_image("ship.bmp")
    sound = games.load_sound("thrust.wav")

    # Константы для управления движением корабля
    ROTATION_STEP = 3  # Шаг вращения при повороте
    VELOCITY_STEP = .03  # Шаг ускорения при движении
    MISSILE_DELAY = 25  # Задержка между выстрелами

    def __init__(self, x, y):
        """ Инициализирует спрайт с изображением корабля. """
        super(Ship, self).__init__(image=Ship.image, x=x, y=y)
        self.missile_wait = 0  # Время до следующего выстрела (начинается с 0)

    def update(self):
        """ Вращает корабль при нажатии клавиш со стрелками. """

        # Если нажата левая стрелка, вращаем корабль влево
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP

        # Если нажата правая стрелка, вращаем корабль вправо
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.ROTATION_STEP

        # Если нажата клавиша "вверх", корабль делает рывок
        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()  # Воспроизводим звук ускорения

            # Изменение скорости по осям X и Y в зависимости от угла корабля
            angle = self.angle * math.pi / 180  # Преобразуем угол в радианы
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)

        # Корабль будет "огибать" экран, то есть появляется с противоположной стороны
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

        # Если нажат пробел, но еще не прошел интервал для следующего выстрела, уменьшаем оставшееся время до выстрела
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # Если нажат пробел и интервал между выстрелами прошел, выпустить ракету
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)  # Добавляем новую ракету на экран
            self.missile_wait = Ship.MISSILE_DELAY  # Устанавливаем новый интервал ожидания для следующего выстрела


class Missile(games.Sprite):
    """ Ракета, которую может выпустить космический корабль игрока. """

    # Изображение ракеты
    image = games.load_image("missile.bmp")

    # Звук, который будет воспроизводиться при запуске ракеты
    sound = games.load_sound("missile.wav")

    # Буфер для расчета начальной позиции ракеты относительно корабля
    BUFFER = 40

    # Скорость ракеты
    VELOCITY_FACTOR = 7

    # Время жизни ракеты
    LIFETIME = 40

    def __init__(self, ship_x, ship_y, ship_angle):
        """ Инициализирует спрайт с изображением ракеты. """

        Missile.sound.play()  # Воспроизводим звук запуска ракеты

        # Преобразование угла из градусов в радианы
        angle = ship_angle * math.pi / 180

        # Вычисление начальной позиции ракеты с учетом угла корабля
        buffer_x = Missile.BUFFER * math.sin(angle)  # Смещение по горизонтали
        buffer_y = Missile.BUFFER * -math.cos(angle)  # Смещение по вертикали
        x = ship_x + buffer_x  # Начальная позиция ракеты по X
        y = ship_y + buffer_y  # Начальная позиция ракеты по Y

        # Вычисление скорости ракеты по осям X и Y с учетом угла
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)

        # Создание ракеты с расчетными значениями
        super(Missile, self).__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)

        # Устанавливаем время жизни ракеты
        self.lifetime = Missile.LIFETIME

    def update(self):
        """ Перемещает ракету. """

        # Уменьшаем оставшееся время жизни ракеты
        self.lifetime -= 1

        # Если время жизни ракеты истекло, уничтожаем ракету
        if self.lifetime == 0:
            self.destroy()

        # Ракета будет огибать экран, т.е. появляется с противоположной стороны
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width


def main():
    # Назначаем фоновую картинку для экрана
    nebula_image = games.load_image("nebula.jpg")
    games.screen.background = nebula_image

    # Создаем 8 астероидов с случайными размерами и позициями
    for i in range(8):
        x = random.randrange(games.screen.width)  # Случайная позиция по X
        y = random.randrange(games.screen.height)  # Случайная позиция по Y
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])  # Случайный размер
        new_asteroid = Asteroid(x=x, y=y, size=size)  # Создаем новый астероид
        games.screen.add(new_asteroid)  # Добавляем астероид на экран

    # Создаем корабль, который будет находиться в центре экрана
    the_ship = Ship(x=games.screen.width / 2, y=games.screen.height / 2)
    games.screen.add(the_ship)  # Добавляем корабль на экран

    # Запускаем главный цикл игры
    games.screen.mainloop()


# Поехали!
main()  # Запускаем игру
