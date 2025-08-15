# Прерванный полет-4
# Корабль начал стрелять ракетами

import math, random
from superwires import games

# Инициализация игрового окна с заданными размерами и частотой обновлений
games.init(screen_width=640, screen_height=480, fps=50)


class Asteroid(games.Sprite):
    """ Астероид, прямолинейно движущийся по экрану. """

    # Константы для разных размеров астероидов
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    # Словарь с изображениями для каждого размера астероида
    images = {SMALL: games.load_image("asteroid_small.bmp"),
              MEDIUM: games.load_image("asteroid_med.bmp"),
              LARGE: games.load_image("asteroid_big.bmp")}

    # Скорость движения астероидов
    SPEED = 2

    def __init__(self, x, y, size):
        """ Инициализирует спрайт с изображением астероида. """
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],  # Загружаем изображение астероида в зависимости от его размера
            x=x, y=y,  # Устанавливаем начальные координаты астероида
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,  # Направление и скорость по оси X
            dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)  # Направление и скорость по оси Y

        self.size = size  # Устанавливаем размер астероида

    def update(self):
        """ Заставляет астероид обогнуть экран. """
        # Если астероид выходит за верхнюю границу экрана, он появляется снизу
        if self.top > games.screen.height:
            self.bottom = 0

        # Если астероид выходит за нижнюю границу экрана, он появляется сверху
        if self.bottom < 0:
            self.top = games.screen.height

        # Если астероид выходит за правую границу экрана, он появляется слева
        if self.left > games.screen.width:
            self.right = 0

        # Если астероид выходит за левую границу экрана, он появляется справа
        if self.right < 0:
            self.left = games.screen.width


class Ship(games.Sprite):
    """ Корабль игрока. """
    image = games.load_image("ship.bmp")  # Загружаем изображение корабля
    sound = games.load_sound("thrust.wav")  # Загружаем звук для рывка
    ROTATION_STEP = 3  # Шаг вращения корабля
    VELOCITY_STEP = .03  # Шаг изменения скорости движения корабля

    def update(self):
        """ Вращает корабль при нажатии клавиш со стрелками. """
        # Если нажата клавиша влево, вращаем корабль влево
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP

        # Если нажата клавиша вправо, вращаем корабль вправо
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.ROTATION_STEP

        # Если нажата клавиша вверх, корабль совершает рывок
        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()  # Воспроизводим звук рывка

            # Изменение горизонтальной и вертикальной скорости корабля с учетом угла поворота
            angle = self.angle * math.pi / 180  # Преобразуем угол в радианы
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)  # Изменяем скорость по оси X
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)  # Изменяем скорость по оси Y

        # Корабль будет "огибать" экран
        # Если корабль выходит за верхнюю границу экрана, он появляется снизу
        if self.top > games.screen.height:
            self.bottom = 0

        # Если корабль выходит за нижнюю границу экрана, он появляется сверху
        if self.bottom < 0:
            self.top = games.screen.height

        # Если корабль выходит за правую границу экрана, он появляется слева
        if self.left > games.screen.width:
            self.right = 0

        # Если корабль выходит за левую границу экрана, он появляется справа
        if self.right < 0:
            self.left = games.screen.width

        # Если нажата клавиша Пробел, выпускаем ракету
        if games.keyboard.is_pressed(games.K_SPACE):
            # Создаем новый объект ракеты с координатами и углом корабля
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)  # Добавляем ракету на экран


class Missile(games.Sprite):
    """ Ракета, которую может выпустить космический корабль игрока. """

    # Загружаем изображение ракеты и звук для выстрела
    image = games.load_image("missile.bmp")
    sound = games.load_sound("missile.wav")

    # Константы для ракеты
    BUFFER = 40  # Расстояние, на которое ракета отстает от корабля при выстреле
    VELOCITY_FACTOR = 7  # Сила, определяющая скорость ракеты
    LIFETIME = 40  # Время жизни ракеты (сколько обновлений экрана ракета существует)

    def __init__(self, ship_x, ship_y, ship_angle):
        """ Инициализирует спрайт с изображением ракеты. """

        Missile.sound.play()  # Воспроизводим звук выстрела ракеты

        # Преобразуем угол корабля в радианы
        angle = ship_angle * math.pi / 180

        # Вычисляем начальную позицию ракеты, которая будет немного смещена от корабля
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x  # Начальная позиция ракеты по оси X
        y = ship_y + buffer_y  # Начальная позиция ракеты по оси Y

        # Вычисляем начальную скорость ракеты по осям X и Y
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)

        # Создаем спрайт ракеты с заданной позицией и скоростью
        super(Missile, self).__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)
        self.lifetime = Missile.LIFETIME  # Устанавливаем время жизни ракеты

    def update(self):
        """ Перемещает ракету. """

        # Уменьшаем время жизни ракеты
        self.lifetime -= 1

        # Если время жизни ракеты истекло, уничтожаем ее
        if self.lifetime == 0:
            self.destroy()

        # Ракета "огибает" экран, то есть, если она выходит за границу экрана, появляется с противоположной стороны
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width


def main():
    # Загружаем изображение фона и устанавливаем его на экран
    nebula_image = games.load_image("nebula.jpg")
    games.screen.background = nebula_image

    # Создаем 8 астероидов с случайными позициями и размерами
    for i in range(8):
        x = random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x=x, y=y, size=size)
        games.screen.add(new_asteroid)  # Добавляем астероид на экран

    # Создаем корабль, помещаем его в центр экрана и добавляем на экран
    the_ship = Ship(image=Ship.image,
                    x=games.screen.width / 2,
                    y=games.screen.height / 2)
    games.screen.add(the_ship)

    # Запускаем игровой цикл
    games.screen.mainloop()


# Поехали!
main()
