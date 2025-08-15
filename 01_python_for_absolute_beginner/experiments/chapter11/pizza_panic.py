# Паника в пиццерии
# Игрок должен ловить падающую пиццу, пока она не достигла земли

from superwires import games, color  # Импортируем нужные библиотеки
import random  # Импортируем модуль для генерации случайных чисел

# Инициализируем графическое окно:
# - ширина экрана 640 пикселей
# - высота экрана 480 пикселей
# - 50 кадров в секунду
games.init(screen_width=640, screen_height=480, fps=50)


class Pan(games.Sprite):
    """
    Сковорода, в которую игрок может ловить падающую пиццу.
    """
    image = games.load_image("pan.bmp")  # Загружаем изображение сковороды

    def __init__(self):
        """ Инициализирует объект Pan и создает объект Text для отображения счета. """
        super(Pan, self).__init__(image=Pan.image,
                                  x=games.mouse.x,  # Начальная позиция сковороды — на месте указателя мыши
                                  bottom=games.screen.height)  # Сковорода должна быть внизу экрана

        # Создаем текстовый объект для отображения счета, его начальное значение 0
        self.score = games.Text(value=0, size=25, color=color.black,
                                top=5, right=games.screen.width - 10)  # Счет в правом верхнем углу
        games.screen.add(self.score)  # Добавляем текст на экран

    def update(self):
        """ Передвигает объект по горизонтали в точку с абсциссой, как у указателя мыши. """
        self.x = games.mouse.x  # Сковорода следует за указателем мыши

        # Ограничиваем движение сковороды, чтобы она не выходила за пределы экрана
        if self.left < 0:
            self.left = 0  # Левая граница сковороды не может выходить за левый край экрана
        if self.right > games.screen.width:
            self.right = games.screen.width  # Правая граница сковороды не может выходить за правый край экрана

        # Проверяем, поймал ли игрок пиццу
        self.check_catch()

    def check_catch(self):
        """ Проверяет, поймал ли игрок падающую пиццу. """
        for pizza in self.overlapping_sprites:  # Если сковорода соприкасается с пиццей
            self.score.value += 10  # Увеличиваем счет на 10
            self.score.right = games.screen.width - 10  # Обновляем позицию счета
            pizza.handle_caught()  # Обрабатываем пойманную пиццу


class Pizza(games.Sprite):
    """
    Круги пиццы, падающие на землю.
    """
    image = games.load_image("pizza.bmp")  # Загружаем изображение пиццы
    speed = 1  # Скорость падения пиццы

    def __init__(self, x, y=90):
        """ Инициализирует объект Pizza """
        super(Pizza, self).__init__(image=Pizza.image,
                                    x=x, y=y,  # Начальные координаты пиццы
                                    dy=Pizza.speed)  # Устанавливаем скорость падения пиццы

    def update(self):
        """ Проверяет, не коснулась ли нижняя кромка спрайта нижней границы экрана. """
        if self.bottom > games.screen.height:  # Если пицца достигла нижней границы экрана
            self.end_game()  # Завершаем игру
            self.destroy()  # Уничтожаем пиццу

    def handle_caught(self):
        """ Разрушает объект, пойманный игроком. """
        self.destroy()  # Уничтожаем пиццу, когда она поймана

    def end_game(self):
        """ Завершает игру. """
        end_message = games.Message(value="Game Over",  # Сообщение о завершении игры
                                    size=90,  # Размер текста
                                    color=color.red,  # Цвет текста
                                    x=games.screen.width / 2,  # Центр экрана по горизонтали
                                    y=games.screen.height / 2,  # Центр экрана по вертикали
                                    lifetime=5 * games.screen.fps,  # Время отображения сообщения
                                    after_death=games.screen.quit)  # После окончания игры закрыть экран
        games.screen.add(end_message)  # Отображаем сообщение на экране


class Chef(games.Sprite):
    """
    Кулинар, который, двигаясь влево-вправо, разбрасывает пиццу.
    """
    image = games.load_image("chef.bmp")  # Загружаем изображение шефа

    def __init__(self, y=55, speed=2, odds_change=200):
        """ Инициализирует объект Chef."""
        # Создаем объект шефа с начальной позицией по оси X в центре экрана и заданной скоростью движения
        super(Chef, self).__init__(image=Chef.image,
                                   x=games.screen.width / 2,  # Начальная позиция по X в центре экрана
                                   y=y,  # Начальная позиция по Y (высота шефа)
                                   dx=speed)  # Начальная скорость по горизонтали

        self.odds_change = odds_change  # Вероятность смены направления
        self.time_til_drop = 0  # Время до следующего сброса пиццы

    def update(self):
        """ Определяет, надо ли сменить направление движения. """
        # Проверяем, если шеф касается левой или правой границы экрана, меняем направление
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        # Также с определенной вероятностью меняем направление
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx

        # Проверяем, нужно ли сбрасывать пиццу
        self.check_drop()

    def check_drop(self):
        """ Уменьшает интервал ожидания на единицу или сбрасывает очередную пиццу и восстанавливает исходный интервал. """
        # Если еще не пришло время сбрасывать пиццу, уменьшаем таймер
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            # Сбрасываем пиццу в позицию шефа
            new_pizza = Pizza(x=self.x)  # Новая пицца появляется по горизонтальной позиции шефа
            games.screen.add(new_pizza)  # Добавляем пиццу на экран

            # Восстанавливаем интервал сброса пиццы. Увеличиваем его в зависимости от высоты пиццы и ее скорости
            self.time_til_drop = int(new_pizza.height * 1.3 / Pizza.speed) + 1


def main():
    """ Собственно игровой процесс. """
    # Загружаем фоновое изображение
    wall_image = games.load_image("wall.jpg", transparent=False)
    games.screen.background = wall_image  # Устанавливаем его как фон

    # Создаем и добавляем шефа на экран
    the_chef = Chef()
    games.screen.add(the_chef)

    # Создаем и добавляем сковороду на экран
    the_pan = Pan()
    games.screen.add(the_pan)

    # Скрываем указатель мыши
    games.mouse.is_visible = False

    # Блокируем события мыши, чтобы не выходить за пределы экрана
    games.screen.event_grab = True

    # Запускаем главный цикл игры
    games.screen.mainloop()


# начнем!
main()  # Запускаем игру
