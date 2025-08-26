import numpy as np
import matplotlib.pyplot as plt

from .plot_points import plot_points


def plot_regressor(
        features,
        labels,
        model,
        *,
        point_size=80,
        xlabel=None,
        ylabel=None,
        xlim=None,
        ylim=None,
        ax=None
):
    """
    Визуализация регрессионной модели вместе с исходными точками данных.

    Parameters
    ----------
    model : object
        Объект модели, реализующий метод `.predict(X)`.
    features : array-like, shape (n_samples,) or (n_samples, 1)
        Массив признаков (одномерный).
    labels : array-like, shape (n_samples,)
        Массив целевых значений (y).
    point_size : int, optional
        Размер точек (по умолчанию 80).
    color_points : str, optional
        Цвет точек исходных данных (по умолчанию "cyan").
    color_line : str, optional
        Цвет линии регрессии (по умолчанию "magenta").
    xlabel : str, optional
        Подпись оси X. Если None → "Feature".
    ylabel : str, optional
        Подпись оси Y. Если None → "Target".
    xlim : tuple[float, float], optional
        Границы оси X. Если None → вычисляются автоматически.
    ylim : tuple[float, float], optional
        Границы оси Y. Если None → вычисляются автоматически.
    ax : matplotlib.axes.Axes, optional
        Ось для отрисовки. Если None → используется текущая.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Ось с построенным графиком.
    """

    X = np.array(features).reshape(-1, 1)
    y = np.array(labels)

    if ax is None:
        ax = plt.gca()

    # Определяем границы X
    if xlim is None:
        x_min, x_max = X.min() - 1, X.max() + 1
    else:
        x_min, x_max = xlim

    resolution = 500  # Количество точек для линии регрессии (по умолчанию 500).

    # Для линии предсказания создаём равномерную сетку
    x_plot = np.linspace(x_min, x_max, resolution).reshape(-1, 1)
    y_pred = model.predict(x_plot)

    color_line = "magenta"

    label_points = "Данные"
    label_line = "Регрессия"

    # Отрисовка данных
    plot_points(X, y,
                point_size=point_size,
                markers=('o', '^'),
                ax=ax)

    # Отрисовка линии регрессии
    ax.plot(x_plot, y_pred,
            color=color_line,
            linewidth=2.5,
            label=label_line,
            zorder=3)

    # Подписи осей
    if xlabel is None:
        xlabel = "Feature"
    if ylabel is None:
        ylabel = "Target"

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Автоматические или кастомные границы
    if ylim is None:
        y_min, y_max = y.min() - 1, y.max() + 1
    else:
        y_min, y_max = ylim

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend()

    return ax
