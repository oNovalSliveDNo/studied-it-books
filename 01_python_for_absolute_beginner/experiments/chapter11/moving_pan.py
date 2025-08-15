# Подвижная сковорода
# Демонстрирует ввод с помощью мыши

from superwires import games  # Импортируем модуль games из библиотеки superwires

# Инициализируем графическое окно:
# - ширина: 640 пикселей
# - высота: 480 пикселей
# - fps (кадров в секунду): 50
games.init(screen_width=640, screen_height=480, fps=50)


class Pan(games.Sprite):
    """ Перемещаемая мышью сковорода. """

    def update(self):
        """
        Обновляет положение сковороды:
        сковорода перемещается туда, где находится указатель мыши.
        """
        self.x = games.mouse.x  # координата X — туда, куда указывает мышь
        self.y = games.mouse.y  # координата Y — туда, куда указывает мышь


def main():
    # Загружаем картинку стены для фона
    wall_image = games.load_image("wall.jpg", transparent=False)
    games.screen.background = wall_image  # Устанавливаем её как фон экрана

    # Загружаем изображение сковороды
    pan_image = games.load_image("pan.bmp")

    # Создаем объект сковороды:
    # - начальная позиция — там, где находится указатель мыши
    the_pan = Pan(image=pan_image,
                  x=games.mouse.x,
                  y=games.mouse.y)

    # Добавляем сковороду на экран
    games.screen.add(the_pan)

    # Скрываем системный курсор мыши
    games.mouse.is_visible = False

    # Перехватываем все события мыши, чтобы они обрабатывались только внутри окна игры
    games.screen.event_grab = True

    # Запускаем главный цикл игры (экран постоянно обновляется)
    games.screen.mainloop()


# поехали! — запускаем программу
main()
