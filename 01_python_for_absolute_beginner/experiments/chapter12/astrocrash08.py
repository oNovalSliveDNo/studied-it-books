# Прерванный полет-8
# Добавлен игровой объект для завершения программы

import math, random
from superwires import games, color

# Инициализация игры с настройками экрана и FPS (количеством кадров в секунду)
games.init(screen_width=640, screen_height=480, fps=50)


class Wrapper(games.Sprite):
    """ Огибатель. Спрайт, который, двигаясь, огибает графический экран. """

    def update(self):
        """ Переносит спрайт на противоположную сторону окна, если тот выходит за границы. """
        # Если спрайт выходит за нижнюю границу экрана, его верхняя граница переносится наверх
        if self.top > games.screen.height:
            self.bottom = 0

        # Если спрайт выходит за верхнюю границу экрана, его нижняя граница переносится вниз
        if self.bottom < 0:
            self.top = games.screen.height

        # Если спрайт выходит за правую границу экрана, его левая граница переносится влево
        if self.left > games.screen.width:
            self.right = 0

        # Если спрайт выходит за левую границу экрана, его правая граница переносится вправо
        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        """ Разрушает объект. """
        self.destroy()  # Уничтожает спрайт с экрана


class Collider(Wrapper):
    """ Погибатель. Огибатель, который может сталкиваться с другими объектами и гибнуть. """

    def update(self):
        """ Проверяет, есть ли спрайты, визуально перекрывающиеся с данным. """
        super(Collider, self).update()  # Обновляем состояние "огибателя", чтобы проверять столкновения

        # Если есть спрайты, которые перекрывают текущий спрайт
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()  # Уничтожаем все спрайты, которые перекрывают текущий
            self.die()  # Уничтожаем сам объект, с которым произошел контакт

    def die(self):
        """ Разрушает объект со взрывом. """
        new_explosion = Explosion(x=self.x, y=self.y)  # Создаем объект взрыва на месте гибели
        games.screen.add(new_explosion)  # Добавляем взрыв на экран
        self.destroy()  # Уничтожаем текущий объект (например, астероид или корабль)


class Asteroid(Wrapper):
    """ Астероид, прямолинейно движущийся по экрану. """

    # Константы для размера астероида
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    # Словарь с изображениями для разных размеров астероидов
    images = {SMALL: games.load_image("asteroid_small.bmp"),
              MEDIUM: games.load_image("asteroid_med.bmp"),
              LARGE: games.load_image("asteroid_big.bmp")}

    # Константы для скорости и спауна астероидов
    SPEED = 2  # скорость движения астероида
    SPAWN = 2  # количество астероидов, которые появляются при разрушении среднего или большого астероида
    POINTS = 30  # количество очков за уничтожение астероида

    total = 0  # Счётчик для общего количества астероидов на экране

    def __init__(self, game, x, y, size):
        """ Инициализирует спрайт с изображением астероида. """
        Asteroid.total += 1  # Увеличиваем общее количество астероидов

        # Создаём астероид с рандомными скоростями по осям x и y в зависимости от его размера
        super(Asteroid, self).__init__(
            image=Asteroid.images[size],  # Загружаем изображение в зависимости от размера
            x=x, y=y,  # Начальная позиция астероида
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,  # Скорость по оси x
            dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)  # Скорость по оси y

        self.game = game  # Игра, к которой принадлежит астероид
        self.size = size  # Размер астероида (маленький, средний или большой)

    def die(self):
        """ Разрушает астероид. """
        Asteroid.total -= 1  # Уменьшаем общее количество астероидов

        # Добавляем очки в зависимости от размера астероида
        self.game.score.value += int(Asteroid.POINTS / self.size)
        # Перемещаем текст с очками в правый верхний угол экрана
        self.game.score.right = games.screen.width - 10

        # Если астероид не маленький, то заменяем его двумя более мелкими астероидами
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(game=self.game,
                                        x=self.x,  # Позиция нового астероида та же
                                        y=self.y,
                                        size=self.size - 1)  # Размер нового астероида на 1 меньше
                games.screen.add(new_asteroid)  # Добавляем новый астероид на экран

        # Если все астероиды уничтожены, переходим на следующий уровень
        if Asteroid.total == 0:
            self.game.advance()  # Переход к следующему уровню

        super(Asteroid, self).die()  # Уничтожаем текущий астероид с экрана


class Ship(Collider):
    """ Корабль игрока. """

    # Загружаем изображение и звук для корабля
    image = games.load_image("ship.bmp")
    sound = games.load_sound("thrust.wav")

    # Константы для управления кораблем
    ROTATION_STEP = 3  # Шаг вращения корабля (угол)
    VELOCITY_STEP = .03  # Шаг ускорения при рывке
    VELOCITY_MAX = 3  # Максимальная скорость корабля
    MISSILE_DELAY = 25  # Задержка перед следующей возможностью выстрела

    def __init__(self, game, x, y):
        """ Инициализирует спрайт с изображением корабля. """
        super(Ship, self).__init__(image=Ship.image, x=x, y=y)  # Инициализируем базовый класс с изображением корабля
        self.game = game  # Игра, в которой находится корабль
        self.missile_wait = 0  # Задержка перед следующим выстрелом ракеты

    def update(self):
        """ Вращает корабль при нажатии клавиш со стрелками. """
        super(Ship, self).update()  # Обновляем положение корабля (если оно изменилось)

        # Вращение корабля влево и вправо
        if games.keyboard.is_pressed(games.K_LEFT):  # Если нажата клавиша влево
            self.angle -= Ship.ROTATION_STEP  # Уменьшаем угол на шаг
        if games.keyboard.is_pressed(games.K_RIGHT):  # Если нажата клавиша вправо
            self.angle += Ship.ROTATION_STEP  # Увеличиваем угол на шаг

        # Корабль совершает рывок, если нажата клавиша вверх
        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()  # Воспроизводим звук рывка

            # Преобразуем угол в радианы и изменяем скорость по осям x и y
            angle = self.angle * math.pi / 180  # Преобразуем угол из градусов в радианы
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)  # Изменение горизонтальной скорости
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)  # Изменение вертикальной скорости

            # Ограничиваем максимальную скорость по осям x и y
            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)  # Ограничиваем скорость по оси x
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)  # Ограничиваем скорость по оси y

        # Если корабль ожидает, когда можно будет снова стрелять, уменьшаем время ожидания
        if self.missile_wait > 0:
            self.missile_wait -= 1  # Уменьшаем задержку

        # Если нажат пробел и можно стрелять (время ожидания истекло), выпустить ракету
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)  # Создаем новую ракету
            games.screen.add(new_missile)  # Добавляем ракету на экран
            self.missile_wait = Ship.MISSILE_DELAY  # Устанавливаем задержку перед следующим выстрелом

    def die(self):
        """ Разрушает корабль и завершает игру. """
        self.game.end()  # Завершаем игру
        super(Ship, self).die()  # Уничтожаем корабль


class Missile(Collider):
    """ Ракета, которую может выпустить космический корабль игрока. """

    # Загружаем изображение и звук для ракеты
    image = games.load_image("missile.bmp")
    sound = games.load_sound("missile.wav")

    # Константы для ракеты
    BUFFER = 40  # Отступ ракеты от корабля
    VELOCITY_FACTOR = 7  # Скорость ракеты
    LIFETIME = 40  # Время жизни ракеты (срок действия)

    def __init__(self, ship_x, ship_y, ship_angle):
        """ Инициализирует спрайт с изображением ракеты. """

        Missile.sound.play()  # Воспроизводим звук запуска ракеты

        # Преобразуем угол корабля в радианы для вычислений
        angle = ship_angle * math.pi / 180  # Преобразование в радианы

        # Вычисление начальной позиции ракеты с учетом отступа (чтобы ракета не выходила из корабля)
        buffer_x = Missile.BUFFER * math.sin(angle)  # Горизонтальный сдвиг
        buffer_y = Missile.BUFFER * -math.cos(angle)  # Вертикальный сдвиг
        x = ship_x + buffer_x  # Новая позиция ракеты по оси X
        y = ship_y + buffer_y  # Новая позиция ракеты по оси Y

        # Вычисление скорости ракеты по осям X и Y
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)  # Горизонтальная скорость ракеты
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)  # Вертикальная скорость ракеты

        # Создаем объект ракеты с вычисленными параметрами
        super(Missile, self).__init__(image=Missile.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)
        self.lifetime = Missile.LIFETIME  # Устанавливаем время жизни ракеты

    def update(self):
        """ Перемещает ракету. """
        super(Missile, self).update()  # Обновляем положение ракеты

        # Уменьшаем время жизни ракеты на каждом шаге
        self.lifetime -= 1  # Уменьшаем оставшееся время жизни

        # Если время жизни ракеты истекло, уничтожаем её
        if self.lifetime == 0:
            self.destroy()  # Уничтожаем ракету


class Explosion(games.Animation):
    """ Анимированный взрыв. """

    # Загружаем звук взрыва
    sound = games.load_sound("explosion.wav")

    # Список изображений для анимации взрыва
    images = ["explosion1.bmp",
              "explosion2.bmp",
              "explosion3.bmp",
              "explosion4.bmp",
              "explosion5.bmp",
              "explosion6.bmp",
              "explosion7.bmp",
              "explosion8.bmp",
              "explosion9.bmp"]

    def __init__(self, x, y):
        """ Инициализация анимации взрыва. """

        # Инициализация анимации взрыва с заданными изображениями и параметрами
        super(Explosion, self).__init__(images=Explosion.images,
                                        x=x, y=y,
                                        repeat_interval=4,  # интервал между кадрами
                                        n_repeats=1,  # анимация будет выполнена один раз
                                        is_collideable=False)  # объект не будет участвовать в столкновениях
        Explosion.sound.play()  # Воспроизводим звук взрыва


class Game(object):
    """ Собственно игра. """

    def __init__(self):
        """ Инициализирует объект Game. """

        # Начальный уровень игры
        self.level = 0

        # Загружаем звук, который будет проигрываться при переходе на следующий уровень
        self.sound = games.load_sound("level.wav")

        # Создание текстового объекта для отображения текущего счета
        self.score = games.Text(value=0,  # Начальный счет равен 0
                                size=30,  # Размер шрифта
                                color=color.white,  # Цвет текста
                                top=5,  # Расположение текста сверху
                                right=games.screen.width - 10,  # Расположение текста справа
                                is_collideable=False)  # Текст не будет участвовать в столкновениях
        games.screen.add(self.score)  # Добавляем текст на экран

        # Создание объекта корабля, которым управляет игрок
        self.ship = Ship(game=self,
                         x=games.screen.width / 2,  # Позиция по оси X в центре экрана
                         y=games.screen.height / 2)  # Позиция по оси Y в центре экрана
        games.screen.add(self.ship)  # Добавляем корабль на экран

    def play(self):
        """ Начинает игру. """

        # Загружаем музыкальную тему для фона и начинаем ее воспроизведение (бесконечно)
        games.music.load("theme.mid")
        games.music.play(-1)

        # Загружаем изображение для фона и устанавливаем его на экран
        nebula_image = games.load_image("nebula.jpg")
        games.screen.background = nebula_image

        # Переход к первому уровню игры
        self.advance()

        # Начало игры, запускаем главный цикл игры
        games.screen.mainloop()

    def advance(self):
        """ Переводит игру на очередной уровень. """

        # Увеличиваем уровень игры на 1
        self.level += 1

        # Задаем минимальное расстояние от корабля до астероидов
        BUFFER = 150

        # Создаем новые астероиды в зависимости от текущего уровня
        for i in range(self.level):
            # Сначала вычисляем минимальные отступы по горизонтали и вертикали
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min

            # Генерируем случайное расстояние от корабля по горизонтали и вертикали
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)

            # Вычисляем координаты астероида на экране
            x = self.ship.x + x_distance
            y = self.ship.y + y_distance

            # Если координаты выходят за пределы экрана, возвращаем объект внутрь окна
            x %= games.screen.width
            y %= games.screen.height

            # Создаем новый астероид с большими размерами на экране
            new_asteroid = Asteroid(game=self,
                                    x=x, y=y,
                                    size=Asteroid.LARGE)
            games.screen.add(new_asteroid)

        # Создаем сообщение, которое будет отображать номер текущего уровня
        level_message = games.Message(value="Уровень " + str(self.level),
                                      size=40,
                                      color=color.yellow,
                                      x=games.screen.width / 2,  # Положение по горизонтали в центре экрана
                                      y=games.screen.width / 10,  # Положение по вертикали
                                      lifetime=3 * games.screen.fps,  # Сообщение будет видно 3 секунды
                                      is_collideable=False)
        games.screen.add(level_message)  # Добавляем сообщение на экран

        # Если это не первый уровень, воспроизводим звук перехода на новый уровень
        if self.level > 1:
            self.sound.play()

    def end(self):
        """ Завершает игру. """

        # Отображаем сообщение 'Game Over' на экране на 5 секунд
        end_message = games.Message(value="Game Over",
                                    size=90,  # Размер шрифта
                                    color=color.red,  # Цвет текста
                                    x=games.screen.width / 2,  # Положение по горизонтали в центре экрана
                                    y=games.screen.height / 2,  # Положение по вертикали в центре экрана
                                    lifetime=5 * games.screen.fps,  # Сообщение будет видно 5 секунд
                                    after_death=games.screen.quit,  # После окончания игры выходим из игры
                                    is_collideable=False)
        games.screen.add(end_message)  # Добавляем сообщение на экран


def main():
    # Создаем объект игры
    astrocrash = Game()

    # Начинаем игру
    astrocrash.play()


# Запуск игры
main()
