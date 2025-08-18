import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay

from .plot_points import plot_points


def plot_dt_decision_boundary(
        model,
        features,
        labels,
        *,
        point_size: int = 80,
        colors=("cyan", "red"),
        class_names=('Class 0', 'Class 1'),
        xlim=None,
        ylim=None,
        ax=None
):
    """
    Визуализирует границу решения классификатора.
    """
    # Создание графика, если не передана ось
    if ax is None:
        ax = plt.gca()

    # Определяем границы
    if xlim is None:
        x_min, x_max = features.iloc[:, 0].min() - 1, features.iloc[:, 0].max() + 1
    else:
        x_min, x_max = xlim

    if ylim is None:
        y_min, y_max = features.iloc[:, 1].min() - 1, features.iloc[:, 1].max() + 1
    else:
        y_min, y_max = ylim

    # Свой colormap - меняем порядок цветов
    custom_cmap = ListedColormap(colors)

    # Строим границу решения
    DecisionBoundaryDisplay.from_estimator(
        model,
        features,
        response_method="predict",
        plot_method="pcolormesh",
        alpha=0.3,
        cmap=custom_cmap,
        ax=ax,
        grid_resolution=200  # чем больше, тем плавнее граница
    )

    plot_points(
        features,
        labels,
        point_size=point_size,
        class_names=class_names,
        xlim=xlim,
        ylim=ylim,
        ax=ax
    )

    # Ограничиваем оси вручную
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    return ax
