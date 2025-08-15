# Прерванный полет-7
# Добавим эффектные взрывы

import math, random
from superwires import games

games.init(screen_width=640, screen_height=480, fps=50)


class Wrapper(games.Sprite):
    """ Огибатель. Спрайт, который, двигаясь, огибает графический экран. """

    def update(self):
        """ Переносит спрайт на противоположную сторону окна, если он выходит за границу экрана. """
        # Если спрайт выходит за нижнюю границу экрана, он появляется сверху
        if self.top > games.screen.height:
            self.bottom = 0

        # Если спрайт выходит за верхнюю границу экрана, он появляется снизу
        if self.bottom < 0:
            self.top = games.screen.height

        # Если спрайт выходит за правую границу экрана, он появляется слева
        if self.left > games.screen.width:
            self.right = 0

        # Если спрайт выходит за левую границу экрана, он появляется справа
        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        """ Разрушает объект. """
        self.destroy()  # Уничтожает спрайт


class Collider(Wrapper):
    """ Погибатель. Огибатель, который может сталкиваться с другими объектами и гибнуть. """

    def update(self):
        """ Проверяет, нет ли спрайтов, визуально перекрывающихся с данным. """
        super(Collider, self).update()  # Обновляем позицию и проверяем огибание экрана

        # Если объект сталкивается с другими спрайтами, то уничтожаем все пересекающиеся объекты
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()  # Уничтожаем пересекающиеся спрайты
            self.die()  # Уничтожаем сам объект

    def die(self):
        """ Разрушает объект со взрывом. """
        new_explosion = Explosion(x=self.x, y=self.y)  # Создаем новый объект взрыва на месте гибели
        games.screen.add(new_explosion)  # Добавляем взрыв на экран
        self.destroy()  # Уничтожаем текущий объект


class Asteroid(Wrapper):
    """ Астероид, прямолинейно движущийся по экрану. """
    SMALL = 1  # Малый размер астероида
    MEDIUM = 2  # Средний размер астероида
    LARGE = 3  # Большой размер астероида
    images = {SMALL: games.load_image("asteroid_small.bmp"),  # Изображение маленького астероида
              MEDIUM: games.load_image("asteroid_med.bmp"),  # Изображение среднего астероида
              LARGE: games.load_image("asteroid_big.bmp")}  # Изображение большого астероида

    SPEED = 2  # Скорость астероида
    SPAWN = 2  # Количество новых астероидов, которые появятся при разрушении

    def __init__(self, x, y, size):
        """ Инициализирует спрайт с изображением астероида. """
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],  # Загружаем изображение астероида в зависимости от его размера
            x=x, y=y,  # Устанавливаем начальные координаты
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,
            # Горизонтальная скорость с учетом размера
            dy=random.choice(
                [1, -1]) * Asteroid.SPEED * random.random() / size)  # Вертикальная скорость с учетом размера

        self.size = size  # Устанавливаем размер астероида

    def die(self):
        """ Разрушает астероид. """
        # Если астероид не маленький, то делим его на два более мелких астероида
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x=self.x,
                                        y=self.y,
                                        size=self.size - 1)  # Создаем новый астероид меньшего размера
                games.screen.add(new_asteroid)  # Добавляем новый астероид на экран
        self.destroy()  # Уничтожаем текущий астероид


class Ship(Collider):
    """ Корабль игрока. """
    image = games.load_image("ship.bmp")  # Изображение корабля
    sound = games.load_sound("thrust.wav")  # Звук ускорения корабля
    ROTATION_STEP = 3  # Шаг поворота при вращении
    VELOCITY_STEP = .03  # Шаг увеличения скорости при движении
    MISSILE_DELAY = 25  # Задержка между выстрелами

    def __init__(self, x, y):
        """ Инициализирует спрайт с изображением корабля. """
        super(Ship, self).__init__(image=Ship.image, x=x, y=y)  # Инициализируем спрайт корабля
        self.missile_wait = 0  # Задержка для следующего выстрела

    def update(self):
        """ Вращает корабль при нажатии клавиш со стрелками и совершает рывок. """
        super(Ship, self).update()  # Обновляем позицию и проверку на столкновения

        # Если нажата клавиша влево, корабль поворачивает влево
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP

        # Если нажата клавиша вправо, корабль поворачивает вправо
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.ROTATION_STEP

        # Если нажата клавиша вверх, корабль совершает рывок
        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()  # Проигрываем звук ускорения

            # Изменяем скорость корабля в зависимости от угла его поворота
            angle = self.angle * math.pi / 180  # Преобразуем угол в радианы
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)  # Горизонтальная скорость
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)  # Вертикальная скорость

        # Если запуск следующей ракеты еще не разрешен, уменьшаем интервал ожидания
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # Если нажата клавиша пробела и интервал ожидания истек, выпустить ракету
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)  # Создаем новую ракету
            games.screen.add(new_missile)  # Добавляем ракету на экран
            self.missile_wait = Ship.MISSILE_DELAY  # Устанавливаем интервал ожидания между выстрелами


class Missile(Collider):
    """ Ракета, которую может выпустить космический корабль игрока. """
    image = games.load_image("missile.bmp")  # Изображение ракеты
    sound = games.load_sound("missile.wav")  # Звук запуска ракеты
    BUFFER = 40  # Буфер, который определяет расстояние от корабля до ракеты
    VELOCITY_FACTOR = 7  # Скорость ракеты
    LIFETIME = 40  # Время жизни ракеты (после этого она уничтожается)

    def __init__(self, ship_x, ship_y, ship_angle):
        """ Инициализирует спрайт с изображением ракеты. """
        Missile.sound.play()  # Проигрываем звук ракеты

        # Преобразование угла корабля в радианы
        angle = ship_angle * math.pi / 180

        # Вычисляем начальную позицию ракеты с учетом угла корабля
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x  # Новая позиция по горизонтали
        y = ship_y + buffer_y  # Новая позиция по вертикали

        # Вычисляем скорость ракеты по осям X и Y
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)

        # Создаем ракету
        super(Missile, self).__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)
        self.lifetime = Missile.LIFETIME  # Устанавливаем время жизни ракеты

    def update(self):
        """ Перемещает ракету. """
        super(Missile, self).update()  # Обновляем позицию ракеты

        # Если "срок годности" ракеты истек, уничтожаем ее
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()  # Уничтожаем ракету


class Explosion(games.Animation):
    """ Анимированный взрыв. """
    sound = games.load_sound("explosion.wav")  # Звук взрыва
    images = ["explosion1.bmp",  # Список изображений для анимации взрыва
              "explosion2.bmp",
              "explosion3.bmp",
              "explosion4.bmp",
              "explosion5.bmp",
              "explosion6.bmp",
              "explosion7.bmp",
              "explosion8.bmp",
              "explosion9.bmp"]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images=Explosion.images,  # Инициализируем анимацию
                                        x=x, y=y,
                                        repeat_interval=4,  # Интервал между кадрами
                                        n_repeats=1,  # Взрыв проигрывается один раз
                                        is_collideable=False)  # Взрыв не взаимодействует с другими объектами
        Explosion.sound.play()  # Проигрываем звук взрыва


def main():
    # назначаем фоновую картинку
    nebula_image = games.load_image("nebula.jpg")  # Загружаем фоновое изображение
    games.screen.background = nebula_image  # Устанавливаем фон на экране

    # создаем 8 астероидов
    for i in range(8):
        x = random.randrange(games.screen.width)  # Случайная позиция по горизонтали
        y = random.randrange(games.screen.height)  # Случайная позиция по вертикали
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])  # Случайный размер астероида
        new_asteroid = Asteroid(x=x, y=y, size=size)  # Создаем новый астероид
        games.screen.add(new_asteroid)  # Добавляем астероид на экран

    # создаем корабль
    the_ship = Ship(x=games.screen.width / 2, y=games.screen.height / 2)  # Создаем корабль в центре экрана
    games.screen.add(the_ship)  # Добавляем корабль на экран

    games.screen.mainloop()  # Запускаем главный цикл игры


# поехали!
main()  # Запуск игры
