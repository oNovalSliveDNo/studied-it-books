import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay

from .plot_points import plot_points


def plot_decision_boundary(
        features,
        labels,
        model_or_func,
        *,
        point_size: int = 80,
        colors=("cyan", "magenta"),
        class_names=("Class 0", "Class 1"),
        xlabel=None,
        ylabel=None,
        xlim=None,
        ylim=None,
        ax=None,
        use_sklearn_display: bool = True
):
    """
    Универсальная функция для отрисовки границы классификации
    (работает с SVM, Keras, деревьями решений и кастомными функциями).

    Parameters
    ----------
    features : array-like, shape (n_samples, 2)
        Матрица признаков.
    labels : array-like, shape (n_samples,)
        Вектор меток классов.
    model_or_func : object или callable
        - Если объект имеет метод .predict → используется для предсказаний (SVM, sklearn, Keras).
        - Если объект совместим с sklearn.inspection.DecisionBoundaryDisplay и use_sklearn_display=True → используется он.
        - Если передана функция f(x, y) → используется напрямую.
    """

    X = np.array(features)
    y = np.array(labels)

    if ax is None:
        ax = plt.gca()

    # Определяем границы
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
        if X.ndim == 1 or (X.ndim == 2 and X.shape[1] == 1):
            y_min = min(X) - 1
            y_max = max(X) + 1
        else:
            y_min = min(X[:, 1]) - 1
            y_max = max(X[:, 1]) + 1
    else:
        y_min, y_max = ylim[0], ylim[1]

    custom_cmap = ListedColormap(colors)

    # Ветка 1: sklearn-овские модели через DecisionBoundaryDisplay
    if use_sklearn_display and hasattr(model_or_func, "predict"):
        try:
            DecisionBoundaryDisplay.from_estimator(
                model_or_func,
                X,
                response_method="predict",
                plot_method="pcolormesh",
                alpha=0.3,
                cmap=custom_cmap,
                ax=ax,
                grid_resolution=300,
                plot_range=[(x_min, x_max), (y_min, y_max)]
            )
        except Exception:
            # Если модель не совместима — fallback к ручной реализации
            use_sklearn_display = False

    # Ветка 2: универсальный fallback (SVM, Keras, функции)
    if not (use_sklearn_display and hasattr(model_or_func, "predict")):
        resolution = 500
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, resolution),
            np.linspace(y_min, y_max, resolution)
        )
        grid = np.c_[xx.ravel(), yy.ravel()]

        if hasattr(model_or_func, "predict"):
            Z = model_or_func.predict(grid)
            if Z.ndim > 1:  # Keras → вероятности
                Z = np.argmax(Z, axis=1)
        else:  # кастомная f(x, y)
            Z = np.array([model_or_func(p[0], p[1]) for p in grid])

        Z = Z.reshape(xx.shape)

        ax.contourf(
            xx, yy, Z,
            levels=np.arange(len(colors) + 1) - 0.5,
            alpha=0.3,
            cmap=custom_cmap
        )
        ax.contour(xx, yy, Z, levels=[0.5], colors="k", linewidths=1.5)

    # Рисуем сами точки
    plot_points(
        X,
        y,
        point_size=point_size,
        colors=colors,
        class_names=class_names,
        xlabel=xlabel,
        ylabel=ylabel,
        xlim=(x_min, x_max),
        ylim=(y_min, y_max),
        ax=ax
    )

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    return ax
