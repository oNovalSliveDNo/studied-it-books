# Прерванный полет-6
# Теперь срабатывают столкновения

import math, random
from superwires import games

games.init(screen_width=640, screen_height=480, fps=50)


class Asteroid(games.Sprite):
    """ Астероид, прямолинейно движущийся по экрану. """

    # Определение размеров астероида
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    # Загрузка изображений астероидов для каждого размера
    images = {SMALL: games.load_image("asteroid_small.bmp"),
              MEDIUM: games.load_image("asteroid_med.bmp"),
              LARGE: games.load_image("asteroid_big.bmp")}

    SPEED = 2  # Скорость движения астероида
    SPAWN = 2  # Количество новых астероидов, которые будут появляться при разрушении

    def __init__(self, x, y, size):
        """ Инициализирует спрайт с изображением астероида. """
        # Создание астероида с указанной позицией и размером
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],
            x=x, y=y,
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,
            dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)

        self.size = size  # Запоминаем размер астероида

    def update(self):
        """ Заставляет астероид обогнуть экран. """
        # Если астероид выходит за верхнюю границу экрана, он появляется внизу
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

    def die(self):
        """ Разрушает астероид. """
        # Если астероид не маленький, то при его уничтожении генерируются два меньших астероида
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x=self.x,
                                        y=self.y,
                                        size=self.size - 1)
                games.screen.add(new_asteroid)  # Добавляем новые астероиды на экран
        # Уничтожаем текущий астероид
        self.destroy()


class Ship(games.Sprite):
    """ Корабль игрока. """

    image = games.load_image("ship.bmp")  # Изображение корабля
    sound = games.load_sound("thrust.wav")  # Звук рывка корабля
    ROTATION_STEP = 3  # Шаг вращения корабля
    VELOCITY_STEP = .03  # Шаг скорости рывка
    MISSILE_DELAY = 25  # Задержка перед следующим выстрелом

    def __init__(self, x, y):
        """ Инициализирует спрайт с изображением корабля. """
        super(Ship, self).__init__(image=Ship.image, x=x, y=y)
        self.missile_wait = 0  # Ожидание между выстрелами

    def update(self):
        """ Вращает корабль при нажатии клавиш со стрелками. """

        # Вращаем корабль с помощью клавиш влево и вправо
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.ROTATION_STEP

        # Если нажата клавиша вверх, корабль совершает рывок
        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()  # Воспроизводим звук рывка

            # Изменяем скорость движения корабля с учетом угла поворота
            angle = self.angle * math.pi / 180  # Преобразуем угол в радианы
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)

        # Корабль будет "огибать" экран, появляться с другой стороны, если выходит за пределы
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width

        # Если запуск ракеты еще не разрешен (задержка), уменьшаем время ожидания
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # Если нажат пробел и прошло достаточно времени для следующего выстрела, запускаем ракету
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)  # Создаем новую ракету
            games.screen.add(new_missile)  # Добавляем ракету на экран
            self.missile_wait = Ship.MISSILE_DELAY  # Устанавливаем задержку перед следующим выстрелом

        # Проверка на столкновение с другими объектами
        if self.overlapping_sprites:  # Если с кораблем есть пересечения
            for sprite in self.overlapping_sprites:  # Для каждого объекта, с которым произошло столкновение
                sprite.die()  # Уничтожаем его
            self.die()  # Уничтожаем сам корабль

    def die(self):
        """ Разрушает корабль. """
        self.destroy()  # Уничтожаем корабль


class Missile(games.Sprite):
    """ Ракета, которую может выпустить космический корабль игрока. """

    image = games.load_image("missile.bmp")  # Изображение ракеты
    sound = games.load_sound("missile.wav")  # Звук выстрела ракеты
    BUFFER = 40  # Расстояние, на котором ракета будет от корабля при старте
    VELOCITY_FACTOR = 7  # Скорость ракеты
    LIFETIME = 40  # Время жизни ракеты до уничтожения

    def __init__(self, ship_x, ship_y, ship_angle):
        """ Инициализирует спрайт с изображением ракеты. """
        Missile.sound.play()  # Воспроизводим звук выстрела ракеты

        # Преобразуем угол в радианы для вычислений
        angle = ship_angle * math.pi / 180

        # Вычисляем начальную позицию ракеты относительно позиции корабля
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y

        # Вычисляем горизонтальную и вертикальную скорость ракеты
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)

        # Создаем ракету с заданной позицией и скоростью
        super(Missile, self).__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)
        self.lifetime = Missile.LIFETIME  # Устанавливаем время жизни ракеты

    def update(self):
        """ Перемещает ракету. """
        # Каждый кадр уменьшаем время жизни ракеты
        self.lifetime -= 1
        # Если срок жизни ракеты истек, уничтожаем её
        if self.lifetime == 0:
            self.destroy()

        # Если ракета выходит за верхнюю границу экрана, она появляется снизу
        if self.top > games.screen.height:
            self.bottom = 0

        # Если ракета выходит за нижнюю границу экрана, она появляется сверху
        if self.bottom < 0:
            self.top = games.screen.height

        # Если ракета выходит за правую границу экрана, она появляется слева
        if self.left > games.screen.width:
            self.right = 0

        # Если ракета выходит за левую границу экрана, она появляется справа
        if self.right < 0:
            self.left = games.screen.width

        # Проверка на столкновения с другими объектами
        if self.overlapping_sprites:  # Если ракета пересекается с другими объектами
            for sprite in self.overlapping_sprites:  # Для каждого объекта, с которым произошло столкновение
                sprite.die()  # Уничтожаем его
            self.die()  # Уничтожаем саму ракету

    def die(self):
        """ Разрушает ракету. """
        self.destroy()  # Уничтожаем ракету


def main():
    # Задаем фоновое изображение игры
    nebula_image = games.load_image("nebula.jpg")
    games.screen.background = nebula_image  # Устанавливаем фоновое изображение на экран

    # Создаем 8 астероидов с случайными координатами и размерами
    for i in range(8):
        x = random.randrange(games.screen.width)  # Случайная позиция по оси X
        y = random.randrange(games.screen.height)  # Случайная позиция по оси Y
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])  # Случайный размер астероида
        new_asteroid = Asteroid(x=x, y=y, size=size)  # Создаем новый астероид
        games.screen.add(new_asteroid)  # Добавляем астероид на экран

    # Создаем корабль игрока и размещаем его по центру экрана
    the_ship = Ship(x=games.screen.width / 2, y=games.screen.height / 2)
    games.screen.add(the_ship)  # Добавляем корабль на экран

    games.screen.mainloop()  # Запускаем главный цикл игры


# Запуск игры!
main()
