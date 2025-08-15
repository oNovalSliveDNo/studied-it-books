# Прерванный полет-1
# Только астероиды движутся по экрану

import random
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
            image=Asteroid.images[size],  # Загружаем изображение в зависимости от размера
            x=x, y=y,  # Начальные координаты
            dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,  # Случайное движение по оси X
            dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)  # Случайное движение по оси Y

        self.size = size  # Устанавливаем размер астероида

    def update(self):
        """ Заставляет астероид обогнуть экран. """
        # Если астероид вышел за верхнюю границу экрана, перемещаем его в нижнюю
        if self.top > games.screen.height:
            self.bottom = 0

        # Если астероид вышел за нижнюю границу экрана, перемещаем его в верхнюю
        if self.bottom < 0:
            self.top = games.screen.height

        # Если астероид вышел за правую границу экрана, перемещаем его в левую
        if self.left > games.screen.width:
            self.right = 0

        # Если астероид вышел за левую границу экрана, перемещаем его в правую
        if self.right < 0:
            self.left = games.screen.width


def main():
    # Назначаем фоновую картинку для игрового экрана
    nebula_image = games.load_image("nebula.jpg")
    games.screen.background = nebula_image

    # Создаем 8 астероидов с случайными координатами и размерами
    for i in range(8):
        x = random.randrange(games.screen.width)  # Случайная позиция по оси X
        y = random.randrange(games.screen.height)  # Случайная позиция по оси Y
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])  # Случайный размер астероида
        new_asteroid = Asteroid(x=x, y=y, size=size)  # Создаем новый астероид
        games.screen.add(new_asteroid)  # Добавляем астероид на экран

    games.screen.mainloop()  # Начинаем игровой цикл


# Запускаем игру!
main()
