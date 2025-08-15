# Читаю с клавиатуры
# Демонстрирует чтение клавиатурного ввода

from superwires import games

# Инициализация игрового окна с заданными размерами и частотой обновлений
games.init(screen_width=640, screen_height=480, fps=50)


class Ship(games.Sprite):
    """ Подвижный космический корабль. """

    def update(self):
        """ Перемещает корабль определенным образом, исходя из нажатых клавиш. """
        # Если нажата клавиша "W", корабль движется вверх
        if games.keyboard.is_pressed(games.K_w):
            self.y -= 1
        # Если нажата клавиша "S", корабль движется вниз
        if games.keyboard.is_pressed(games.K_s):
            self.y += 1
        # Если нажата клавиша "A", корабль движется влево
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 1
        # Если нажата клавиша "D", корабль движется вправо
        if games.keyboard.is_pressed(games.K_d):
            self.x += 1


def main():
    # Загружаем изображение космоса для фона
    nebula_image = games.load_image("nebula.jpg", transparent=False)
    games.screen.background = nebula_image  # Устанавливаем его как фон экрана

    # Загружаем изображение космического корабля
    ship_image = games.load_image("ship.bmp")
    # Создаем космический корабль, помещаем его в центр экрана
    the_ship = Ship(image=ship_image,
                    x=games.screen.width / 2,
                    y=games.screen.height / 2)
    # Добавляем корабль на экран
    games.screen.add(the_ship)

    # Запускаем главный цикл игры
    games.screen.mainloop()


# Начинаем игру
main()
