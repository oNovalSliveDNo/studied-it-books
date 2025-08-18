import numpy as np
import matplotlib.pyplot as plt

from .plot_points import plot_points


def plot_learning_history(
        weights_history,
        bias_history,
        features, labels,
        xlim=None,
        ylim=None,
        ax=None
):
    """
    Визуализирует историю обучения, отображая все промежуточные разделяющие линии.

    Параметры:
        weights_history (list): Список векторов весов на каждом шаге обучения
        bias_history (list): Список значений смещения на каждом шаге обучения
        features (numpy.ndarray): Матрица признаков (используется для определения границ графика)
        ax (matplotlib.axes.Axes, optional): Объект осей для рисования. Если None, используется текущие оси.
        zorder (int, optional): Порядок отрисовки. По умолчанию 0.
    """

    X = np.array(features)
    y = np.array(labels)

    # Если оси не переданы, получаем текущие оси графика
    if ax is None:
        ax = plt.gca()

    # Определяем границы по оси X для рисования линий
    if xlim is None:
        if X.ndim == 1 or (X.ndim == 2 and X.shape[1] == 1):
            x_min = (min(X) - 1)  # Левая граница с отступом 1
            x_max = (max(X) + 1)  # Правая граница с отступом 1
        else:
            x_min = min(X[:, 0]) - 1  # Левая граница с отступом 1
            x_max = max(X[:, 0]) + 1  # Правая граница с отступом 1
    else:
        x_min, x_max = xlim[0], xlim[1]

    if ylim is None:
        y_min = (min(y) - 1)  # Левая граница с отступом 1
        y_max = (max(y) + 1)  # Правая граница с отступом 1
    else:
        y_min, y_max = ylim[0], ylim[1]

    # Рисуем все промежуточные классификаторы из истории обучения
    for i, (weights, bias) in enumerate(zip(weights_history, bias_history)):
        # Вычисляем координаты для разделяющей линии
        # Уравнение линии: w0*x + w1*y + bias = 0 => y = -(w0*x + bias)/w1
        x_values = np.array([x_min, x_max])  # Точки на краях графика
        y_values = -(weights[0] * x_values + bias) / weights[1]

        # Рисуем линию с полупрозрачным серым цветом и тонкой линией
        ax.plot(x_values, y_values,
                color='gray',  # Серый цвет
                alpha=0.1,  # Прозрачность 10%
                linewidth=1,  # Толщина линии 1
                zorder=1)  # Порядок отрисовки

    # Последнюю линию рисуем более заметной (если история не пустая)
    if len(weights_history) > 0:
        final_weights = weights_history[-1]  # Последние веса
        final_bias = bias_history[-1]  # Последнее смещение
        y_values = -(final_weights[0] * x_values + final_bias) / final_weights[1]
        ax.plot(x_values, y_values,
                color='gray',  # Серый цвет
                alpha=0.3,  # Прозрачность 30%
                linewidth=2,  # Толщина линии 2
                label='История обучения')  # Подпись для легенды

    return ax


def plot_classifier(
        weights,
        bias,
        features,
        labels,
        weights_history=None,
        bias_history=None,
        point_size: int = 80,
        colors=("cyan", "red"),
        markers=("s", "^"),
        class_names=("Class 0", "Class 1"),
        xlabel=None,
        ylabel=None,
        xlim=None,
        ylim=None,
        ax=None
):
    """
    Основная функция для визуализации классификатора и данных.

    Параметры:
        weights (numpy.ndarray): Вектор весов обученной модели
        bias (float): Смещение обученной модели
        features (numpy.ndarray): Матрица признаков
        labels (numpy.ndarray): Вектор меток классов
        x (numpy.ndarray): Координаты точек по оси X
        y (numpy.ndarray): Координаты точек по оси Y
        weights_history (list, optional): История весов в процессе обучения. По умолчанию None.
        bias_history (list, optional): История смещений в процессе обучения. По умолчанию None.
        ax (matplotlib.axes.Axes, optional): Объект осей для рисования. По умолчанию None.
    """

    X = np.array(features)
    y = np.array(labels)

    # Если оси не переданы, получаем текущие оси графика
    if ax is None:
        ax = plt.gca()

    # Определяем границы по оси X для рисования линий
    if xlim is None:
        if X.ndim == 1 or (X.ndim == 2 and X.shape[1] == 1):
            x_min = (min(X) - 1)  # Левая граница с отступом 1
            x_max = (max(X) + 1)  # Правая граница с отступом 1
        else:
            x_min = min(X[:, 0]) - 1  # Левая граница с отступом 1
            x_max = max(X[:, 0]) + 1  # Правая граница с отступом 1
    else:
        x_min, x_max = xlim[0], xlim[1]

    if ylim is None:
        y_min = (min(y) - 1)  # Левая граница с отступом 1
        y_max = (max(y) + 1)  # Правая граница с отступом 1
    else:
        y_min, y_max = ylim[0], ylim[1]

    # 1. Сначала рисуем историю линий (если передана)
    if weights_history is not None and bias_history is not None:
        plot_learning_history(weights_history, bias_history, X, y, xlim, ylim, ax=ax)

    # 2. Затем рисуем точки данных (чтобы они были поверх линий истории)
    plot_points(X, y,
                point_size=point_size,
                colors=colors,
                markers=markers,
                class_names=class_names,
                xlabel=xlabel,
                ylabel=ylabel,
                ax=ax)

    # 3. И только потом рисуем финальную линию классификатора (чтобы она была поверх всего)
    x_values = np.array([x_min, x_max])  # От края до края с отступами
    y_values = -(weights[0] * x_values + bias) / weights[1]  # Уравнение разделяющей линии

    # Рисуем финальную линию классификатора
    ax.plot(x_values, y_values, 'k-', linewidth=4, label='Финальный классификатор', zorder=3)

    # Настраиваем границы графика
    ax.set_xlim(x_min, x_max)  # Границы по X с отступами
    ax.set_ylim(y_min, y_max)  # Границы по Y с отступами

    return ax
