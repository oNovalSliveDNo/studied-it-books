# Взрыв
# Демонстрирует создание анимации

from superwires import games

# Инициализация игрового окна с заданными размерами и частотой обновлений
games.init(screen_width=640, screen_height=480, fps=50)

# Загружаем изображение космоса для фона
nebula_image = games.load_image("nebula.jpg", transparent=0)
games.screen.background = nebula_image  # Устанавливаем его как фон экрана

# Список файлов с изображениями кадров анимации взрыва
explosion_files = ["explosion1.bmp",
                   "explosion2.bmp",
                   "explosion3.bmp",
                   "explosion4.bmp",
                   "explosion5.bmp",
                   "explosion6.bmp",
                   "explosion7.bmp",
                   "explosion8.bmp",
                   "explosion9.bmp"]

# Создание анимации взрыва. Анимация будет повторяться бесконечно с интервалом 5 кадров
explosion = games.Animation(images=explosion_files,
                            x=games.screen.width / 2,  # Устанавливаем анимацию в центр экрана
                            y=games.screen.height / 2,
                            n_repeats=0,  # Бесконечное повторение
                            repeat_interval=5)  # Интервал между кадрами анимации

# Добавляем анимацию взрыва на экран
games.screen.add(explosion)

# Запускаем главный цикл игры
games.screen.mainloop()
