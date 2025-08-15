# Летающая пицца
# Демонстрирует движущиеся спрайты

from superwires import games  # Импортируем модуль games из библиотеки superwires для работы с графикой и анимацией

# Инициализируем графическое окно:
# - ширина 640 пикселей
# - высота 480 пикселей
# - fps (кадров в секунду) = 50 — как часто обновляется экран
games.init(screen_width=640, screen_height=480, fps=50)

# Загружаем картинку стены (фона)
# transparent=False — изображение не будет прозрачным
wall_image = games.load_image("wall.jpg", transparent=False)
games.screen.background = wall_image  # Устанавливаем картинку как фон экрана

# Загружаем изображение пиццы
pizza_image = games.load_image("pizza.bmp")

# Создаем спрайт пиццы:
# - image — используем картинку пиццы
# - x, y — начальная позиция в центре экрана
# - dx, dy — скорость по горизонтали и вертикали (1 пиксель за кадр)
the_pizza = games.Sprite(image=pizza_image,
                         x=games.screen.width / 2,
                         y=games.screen.height / 2,
                         dx=1,  # движение вправо
                         dy=1)  # движение вниз

# Добавляем пиццу на экран, чтобы она появилась и начала двигаться
games.screen.add(the_pizza)

# Запускаем главный цикл — окно работает и обновляется каждый кадр
games.screen.mainloop()
