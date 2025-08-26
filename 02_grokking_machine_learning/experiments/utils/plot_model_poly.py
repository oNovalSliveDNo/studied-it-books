import numpy as np
import matplotlib.pyplot as plt
from models.polynomial_regression import predict_polynomial


def plot_model_poly(
        weights,
        degree,
        features,
        labels,
        ax=None):
    """
    Строит график полиномиальной модели и точек выборки

    Parameters:
        weights (list or np.array): Коэффициенты полинома
        degree (int): Степень полинома
        features (array-like): Массив входных значений x
        labels (array-like): Массив фактических значений y
    """

    if ax is None:
        ax = plt.gca()

    x_line = np.linspace(min(features), max(features), 100)  # Плавная линия по x
    y_line = predict_polynomial(weights, x_line, degree)  # Вычисляем y по полиному

    ax.plot(x_line, y_line, label="Модель", color="red", zorder=3)  # Линия модели
    ax.set_title(f"Полиномиальная регрессия (degree={degree})")
    ax.legend()
    ax.grid(True)

    return ax
