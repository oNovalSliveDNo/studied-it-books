import numpy as np
import matplotlib.pyplot as plt


def plot_points(
        features,
        labels,
        *,
        point_size: int = 80,
        colors=("cyan", "magenta"),
        markers=("s", "^"),
        class_names=("Class 0", "Class 1"),
        xlabel=None,
        ylabel=None,
        legend=True,
        xlim=None,
        ylim=None,
        ax=None
):
    """
    Универсальная функция для отображения точек данных
    (подходит и для регрессии, и для классификации).

    Args:
        features: Массив признаков (1D или 2D).
        labels: Массив меток (0/1 или значения целевой переменной).
        point_size: Размер точек (по умолчанию 80).
        colors: Цвета для классов (Class 1, Class 0).
        markers: Маркеры для классов.
        class_names: Имена классов для легенды.
        xlabel: Подпись оси X.
        ylabel: Подпись оси Y.
        legend: Добавлять ли легенду.
        ax: Объект matplotlib Axes для отрисовки.
    """

    X = np.array(features)
    y = np.array(labels)

    if ax is None:
        ax = plt.gca()

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

    # Случай 1: регрессия (одномерные признаки)
    if X.ndim == 1 or (X.ndim == 2 and X.shape[1] == 1):
        ax.scatter(X, y, s=point_size, color=colors[0], edgecolor="k", marker=markers[0], zorder=1)
        if xlabel is None: xlabel = "Feature"
        if ylabel is None: ylabel = "Target"

    # Случай 2: классификация (двумерные признаки)
    else:

        class0 = X[y == 0]
        class1 = X[y == 1]

        ax.scatter(class0[:, 0],
                   class0[:, 1],
                   s=point_size,
                   color=colors[0],
                   edgecolor="k",
                   marker=markers[0],
                   label=class_names[0],
                   zorder=1)

        ax.scatter(class1[:, 0],
                   class1[:, 1],
                   s=point_size,
                   color=colors[1],
                   edgecolor="k",
                   marker=markers[1],
                   label=class_names[1],
                   zorder=2)

        if xlabel is None: xlabel = "x₁"
        if ylabel is None: ylabel = "x₂"

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if legend and X.ndim > 1:
        ax.legend()

    ax.grid(True, linestyle='--', alpha=0.7)

    # Настраиваем границы графика
    ax.set_xlim(x_min, x_max)  # Границы по X с отступами
    ax.set_ylim(y_min, y_max)  # Границы по Y с отступами

    return ax
