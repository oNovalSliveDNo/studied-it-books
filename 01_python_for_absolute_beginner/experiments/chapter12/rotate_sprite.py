# Крутящийся спрайт
# Демонстрирует вращение спрайта

from superwires import games

# Инициализация игрового окна с заданными размерами и частотой обновлений
games.init(screen_width=640, screen_height=480, fps=50)


class Ship(games.Sprite):
    """ Вращающийся космический корабль. """

    def update(self):
        """ Вращает корабль определенным образом, исходя из нажатых клавиш. """
        # Если нажата клавиша "вправо", увеличиваем угол вращения корабля
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += 1
        # Если нажата клавиша "влево", уменьшаем угол вращения корабля
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= 1

        # Если нажата клавиша "1", устанавливаем угол вращения в 0° (начальная ориентация)
        if games.keyboard.is_pressed(games.K_1):
            self.angle = 0
        # Если нажата клавиша "2", устанавливаем угол вращения в 90°
        if games.keyboard.is_pressed(games.K_2):
            self.angle = 90
        # Если нажата клавиша "3", устанавливаем угол вращения в 180°
        if games.keyboard.is_pressed(games.K_3):
            self.angle = 180
        # Если нажата клавиша "4", устанавливаем угол вращения в 270°
        if games.keyboard.is_pressed(games.K_4):
            self.angle = 270


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
