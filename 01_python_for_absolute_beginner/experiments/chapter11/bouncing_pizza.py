# Скачущая пицца
# Демонстрирует обработку столкновений с границами экрана

from superwires import games  # Импортируем games из библиотеки superwires для работы с графикой

# Настраиваем графическое окно:
# - ширина: 640 пикселей
# - высота: 480 пикселей
# - fps: 50 (кадров в секунду, т.е. частота обновления экрана)
games.init(screen_width=640, screen_height=480, fps=50)


class Pizza(games.Sprite):
    """ Скачущая пицца. """

    def update(self):
        """
        Проверяет, не вышла ли пицца за границы экрана.
        Если вышла — меняет направление движения (отскакивает).
        """
        # Проверка по горизонтали:
        # если пицца ушла за правую или левую границу — меняем направление по X
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx  # Инвертируем скорость по X

        # Проверка по вертикали:
        # если пицца ушла за верхнюю или нижнюю границу — меняем направление по Y
        if self.bottom > games.screen.height or self.top < 0:
            self.dy = -self.dy  # Инвертируем скорость по Y


def main():
    # Загружаем фоновое изображение стены
    wall_image = games.load_image("wall.jpg", transparent=False)
    games.screen.background = wall_image  # Устанавливаем его как фон

    # Загружаем изображение пиццы
    pizza_image = games.load_image("pizza.bmp")

    # Создаем объект пиццы:
    # - в центре экрана (x и y — половина ширины и высоты)
    # - dx = 1 — движение вправо
    # - dy = 1 — движение вниз
    the_pizza = Pizza(image=pizza_image,
                      x=games.screen.width / 2,
                      y=games.screen.height / 2,
                      dx=1,
                      dy=1)

    # Добавляем пиццу на экран
    games.screen.add(the_pizza)

    # Запускаем главный игровой цикл (обновление экрана)
    games.screen.mainloop()


# поехали! — запускаем игру
main()
