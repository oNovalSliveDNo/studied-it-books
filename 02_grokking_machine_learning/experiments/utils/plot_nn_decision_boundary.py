import numpy as np
import matplotlib.pyplot as plt


# Функция для визуализации границы принятия решений
def plot_nn_decision_boundary(f, xlim, ylim, happy, sad):
    """
    Функция рисует точки датасета и границу решений для переданной функции f(x, y).
    f — это модель, которая принимает два числа (a, b) и возвращает вероятность или метку класса.
    """

    # Вспомогательная функция для преобразования выхода в бинарный класс
    def h(x, y):  # Функция-помощник: возвращает True (1), если вероятность >= 0.5
        return f(x, y) >= 0.5  # порог 0.5 для бинарной классификации

    # Создаем сетку точек для построения границы в диапазоне от -0.5 до 3.0 по обеим осям
    xx, yy = np.meshgrid(np.arange(xlim[0], xlim[1], 0.005),  # шаг по X
                         np.arange(ylim[0], ylim[1], 0.005))  # шаг по Y

    # Вычисляем предсказания для каждой точки сетки
    Z = np.array([h(i[0], i[1]) for i in np.c_[xx.ravel(), yy.ravel()]])
    Z = Z.reshape(xx.shape)

    # 1. Сначала рисуем заливку областей (zorder=1)
    plt.contourf(xx, yy, Z, colors=['red', 'green'], alpha=0.25,
                 levels=range(-1, 2), zorder=1)

    # 2. Затем рисуем границу между областями (zorder=2)
    plt.contour(xx, yy, Z, colors='k', linewidths=3, zorder=2)

    # 3. Рисуем точки поверх всего (zorder=3) с черной границей
    plt.scatter(happy['Aaк'], happy['Бип'], c='green', ec='black',
                linewidth=1, label='Радостный', s=300, zorder=3)

    plt.scatter(sad['Aaк'], sad['Бип'], c='red', ec='black',
                linewidth=1, label='Грустный', s=300, zorder=3)

    # Настраиваем оси и заголовок
    plt.xlabel('Количество "Аак"')
    plt.ylabel('Количество "Бип"')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.4, zorder=0)
