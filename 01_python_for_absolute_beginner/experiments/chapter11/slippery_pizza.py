# Ускользающая пицца
# Демонстрирует проверку на соприкосновение спрайтов

from superwires import games  # Импортируем модуль games из библиотеки superwires
import random  # Импортируем модуль для генерации случайных чисел

# Инициализируем графическое окно:
# - ширина: 640 пикселей
# - высота: 480 пикселей
# - fps (кадров в секунду): 50
games.init(screen_width=640, screen_height=480, fps=50)


class Pan(games.Sprite):
    """ Сковорода, которую можно мышью перемещать по экрану. """

    def update(self):
        """
        Обновляет положение сковороды: она следует за мышью.
        Также запускает проверку на столкновение с пиццей.
        """
        self.x = games.mouse.x  # Перемещаем по оси X в точку, где мышь
        self.y = games.mouse.y  # Перемещаем по оси Y в точку, где мышь
        self.check_collide()  # Проверяем столкновение с пиццей

    def check_collide(self):
        """
        Проверяет, соприкасается ли сковорода с другими спрайтами (в нашем случае — с пиццей).
        Если да — пицца убегает (меняет координаты).
        """
        for pizza in self.overlapping_sprites:  # Проверяем все спрайты, с которыми соприкасается сковорода
            pizza.handle_collide()  # Если есть соприкосновение, обрабатываем его


class Pizza(games.Sprite):
    """ Ускользающая пицца. """

    def handle_collide(self):
        """
        При соприкосновении со сковородой пицца перемещается в случайное место на экране.
        """
        self.x = random.randrange(games.screen.width)  # Случайная координата X
        self.y = random.randrange(games.screen.height)  # Случайная координата Y


def main():
    # Загружаем изображение фона и устанавливаем его
    wall_image = games.load_image("wall.jpg", transparent=False)
    games.screen.background = wall_image

    # Загружаем картинку пиццы
    pizza_image = games.load_image("pizza.bmp")
    # Определяем случайные координаты появления пиццы
    pizza_x = random.randrange(games.screen.width)
    pizza_y = random.randrange(games.screen.height)
    # Создаем объект пиццы и добавляем его на экран
    the_pizza = Pizza(image=pizza_image, x=pizza_x, y=pizza_y)
    games.screen.add(the_pizza)

    # Загружаем картинку сковороды
    pan_image = games.load_image("pan.bmp")
    # Создаем объект сковороды, устанавливаем в точку курсора мыши
    the_pan = Pan(image=pan_image,
                  x=games.mouse.x,
                  y=games.mouse.y)
    games.screen.add(the_pan)

    # Скрываем курсор мыши, чтобы его не было видно в игре
    games.mouse.is_visible = False

    # Захватываем события мыши (чтобы мышь не выходила за пределы окна игры)
    games.screen.event_grab = True

    # Запускаем главный игровой цикл
    games.screen.mainloop()


# поехали! — запускаем игру
main()
