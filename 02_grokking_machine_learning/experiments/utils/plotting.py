# chapter05/utils/plotting.py


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from typing import Union, Sequence, Tuple
from sklearn.inspection import DecisionBoundaryDisplay

from models.polynomial_regression import predict_polynomial


def plot_errors(errors_list, error_name):
    """
    Строит график ошибок по эпохам обучения

    Parameters:
        errors_list (list): Список значений ошибки (например, RMSE на каждой эпохе)
        error_name (str): Название ошибки (для отображения в заголовке)
    """
    plt.scatter(range(len(errors_list)), errors_list, s=8)
    plt.title(f"{error_name.upper()} по эпохам")
    plt.xlabel("Эпоха")
    plt.ylabel(error_name.upper())
    plt.grid(True)
    plt.show()


def plot_model_poly(weights, degree, features, labels):
    """
    Строит график полиномиальной модели и точек выборки

    Parameters:
        weights (list or np.array): Коэффициенты полинома
        degree (int): Степень полинома
        features (array-like): Массив входных значений x
        labels (array-like): Массив фактических значений y
    """
    x_line = np.linspace(min(features), max(features), 100)  # Плавная линия по x
    y_line = predict_polynomial(weights, x_line, degree)  # Вычисляем y по полиному

    plt.plot(x_line, y_line, label="Модель", color="green")  # Линия модели
    plt.scatter(features, labels, label="Точки", color="blue")  # Исходные точки
    plt.title(f"Полиномиальная регрессия (degree={degree})")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_points(
        features: Union[np.ndarray, pd.DataFrame, Sequence[Sequence[float]]],
        labels: Union[np.ndarray, pd.Series, Sequence[int]],
        *,
        class_names: Sequence[str] = ("Class 1", "Class 0"),
        colors: Sequence[str] = ("#00bcd4",  # красный
                                 "#f44336"),  # голубой
        markers: Sequence[str] = ("^",  # треугольник
                                  "s"),  # квадрат
        sizes: Sequence[int] = (80, 80),
        figsize: Tuple[int, int] = (6, 6),
        ax: plt.Axes = None,
) -> plt.Axes:
    """
    Отображает точки данных двух классов на 2D-плоскости.

    Parameters
    ----------
    features : array-like, shape (n_samples, 2)
        Матрица признаков с двумя столбцами (x1, x2).
    labels : array-like, shape (n_samples,)
        Массив меток классов (0 или 1).
    class_names : tuple of str, optional
        Названия классов для легенды (по умолчанию: ("Class 1", "Class 0")).
    colors : tuple of str, optional
        Цвета маркеров для классов (по умолчанию: бирюзовый и красный).
    markers : tuple of str, optional
        Формы маркеров для классов (по умолчанию: треугольник и квадрат).
    sizes : tuple of int, optional
        Размеры маркеров для классов.
    ax : matplotlib.axes.Axes, optional
        Объект осей для рисования. Если не указан — создаётся новый.

    Returns
    -------
    matplotlib.axes.Axes
        Объект осей с нарисованными точками.
    """
    X = np.asarray(features)
    y = np.asarray(labels)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)  # Используем figsize

    # Определяем подписи осей
    if isinstance(features, pd.DataFrame):
        # Используем имена столбцов DataFrame
        xlabel = features.columns[0] if X.shape[1] > 0 else "x"
        ylabel = features.columns[1] if X.shape[1] > 1 else "y"
    else:
        # Генерируем стандартные имена x₁, x₂, ...
        xlabel = "x₁" if X.shape[1] > 0 else "x"
        ylabel = "x₂" if X.shape[1] > 1 else "y"

    # 1D случай (x - признак, y - метка)
    if X.ndim == 1 or X.shape[1] == 1:
        ax.scatter(X, y, color=colors[0], s=sizes[0], edgecolor="black", zorder=3)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("y" if not isinstance(labels, pd.Series) else labels.name or "y")
        ax.grid(True, linestyle="--", alpha=0.5)
        return ax

    # 2D случай (два (x1, x2) признака + (y) классы)
    for class_value, color, marker, size, name in zip(
            (1, 0), colors, markers, sizes, class_names
    ):
        mask = y == class_value
        ax.scatter(
            X[mask, 0],
            X[mask, 1],
            c=color,
            edgecolor="black",
            marker=marker,
            s=size,
            label=name,
            linewidth=0.8,
            zorder=3
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_aspect("equal", adjustable="box")

    return ax


def plot_model(
        X: Union[np.ndarray, pd.DataFrame, Sequence[Sequence[float]]],
        y: Union[np.ndarray, pd.Series, Sequence[int]],
        model,
        plot_step: float = 0.01,
        alpha: float = 0.2,
        colors=("#f44336", "#00bcd4"),
        figsize: Tuple[int, int] = (6, 6),
        ax: plt.Axes = None
) -> plt.Axes:
    """
    Визуализирует границу решений модели классификации вместе с данными.

    Parameters
    ----------
    X : array-like, shape (n_samples, 2)
        Матрица признаков (должна быть двумерной).
    y : array-like, shape (n_samples,)
        Массив меток классов (0 или 1).
    model : object
        Объект модели, имеющий метод `predict`.
    plot_step : float, optional
        Шаг сетки для построения границы решений.
    alpha : float, optional
        Прозрачность заливки областей решений.

    Returns
    -------
    None
    """
    X = np.asarray(X)
    y = np.asarray(y)

    # Определяем границы графика
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

    # Создаём сетку точек
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, plot_step),
        np.arange(y_min, y_max, plot_step)
    )

    # Предсказываем для каждой точки сетки
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    cmap = ListedColormap(colors)

    # Заливаем области решений
    ax.contourf(xx, yy, Z, cmap=cmap, alpha=alpha, zorder=1)

    # Рисуем границы решений
    ax.contour(xx, yy, Z, colors="black", linewidths=1, zorder=5)

    # Рисуем исходные точки
    plot_points(X, y, ax=ax)

    return ax


# def plot_points(features, labels, x=None, y=None, ax=None, zorder=0):
#     """
#     Визуализирует точки данных на графике с разными маркерами для разных классов.
#
#     Параметры:
#         features (numpy.ndarray): Матрица признаков (не используется напрямую, но нужен для совместимости)
#         labels (numpy.ndarray): Вектор меток классов (0 или 1)
#         x (numpy.ndarray): Координаты точек по оси X
#         y (numpy.ndarray): Координаты точек по оси Y
#         ax (matplotlib.axes.Axes, optional): Объект осей для рисования. Если None, используется текущие оси.
#         zorder (int, optional): Порядок отрисовки (чем больше, тем "выше" элемент). По умолчанию 0.
#     """
#     # Если оси не переданы, получаем текущие оси графика
#     if ax is None:
#         ax = plt.gca()
#
#     # Рисуем точки для класса 0 (метка 0)
#     # marker='s' - квадратные маркеры
#     # s=300 - размер маркеров
#     # c='blue' - синий цвет
#     # label='Грустный (0)' - подпись для легенды
#     ax.scatter(x[labels == 0], y[labels == 0],
#                marker='s', s=300, c='blue', label='Грустный (0)', zorder=zorder)
#
#     # Рисуем точки для класса 1 (метка 1)
#     # marker='^' - треугольные маркеры
#     # c='orange' - оранжевый цвет
#     # label='Радостный (1)' - подпись для легенды
#     ax.scatter(x[labels == 1], y[labels == 1],
#                marker='^', s=300, c='orange', label='Радостный (1)', zorder=zorder)


def plot_learning_history(weights_history, bias_history, features, ax=None, zorder=0):
    """
    Визуализирует историю обучения, отображая все промежуточные разделяющие линии.

    Параметры:
        weights_history (list): Список векторов весов на каждом шаге обучения
        bias_history (list): Список значений смещения на каждом шаге обучения
        features (numpy.ndarray): Матрица признаков (используется для определения границ графика)
        ax (matplotlib.axes.Axes, optional): Объект осей для рисования. Если None, используется текущие оси.
        zorder (int, optional): Порядок отрисовки. По умолчанию 0.
    """
    # Если оси не переданы, получаем текущие оси графика
    if ax is None:
        ax = plt.gca()

    # Определяем границы по оси X для рисования линий
    x_min = min(features[:, 0]) - 0.5  # Левая граница с отступом 0.5
    x_max = max(features[:, 0]) + 0.5  # Правая граница с отступом 0.5

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
                zorder=zorder)  # Порядок отрисовки

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


def plot_classifier(weights, bias, features, labels, x, y, weights_history=None, bias_history=None, ax=None):
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
    # Если оси не переданы, получаем текущие оси графика
    if ax is None:
        ax = plt.gca()

    # 1. Сначала рисуем историю линий (если передана)
    if weights_history is not None and bias_history is not None:
        plot_learning_history(weights_history, bias_history, features, ax=ax, zorder=0)

    # 2. Затем рисуем точки данных (чтобы они были поверх линий истории)
    plot_points(features, labels, x, y, ax=ax, zorder=1)

    # 3. И только потом рисуем финальную линию классификатора (чтобы она была поверх всего)
    x_values = np.array([min(x) - 0.5, max(x) + 0.5])  # От края до края с отступами
    y_values = -(weights[0] * x_values + bias) / weights[1]  # Уравнение разделяющей линии

    # Рисуем финальную линию классификатора
    # 'k-' - черная сплошная линия
    # linewidth=4 - толщина линии 4
    # label='Финальный классификатор' - подпись для легенды
    # zorder=2 - рисуем поверх других элементов
    ax.plot(x_values, y_values, 'k-', linewidth=4, label='Финальный классификатор', zorder=2)

    # Настраиваем границы графика
    ax.set_xlim(min(x) - 0.5, max(x) + 0.5)  # Границы по X с отступами
    ax.set_ylim(min(y) - 0.5, max(y) + 0.5)  # Границы по Y с отступами


def plot_error_history(errors_list):
    """
    Визуализирует график изменения ошибки в процессе обучения.

    Параметры:
        errors_list (list): Список значений ошибки на каждом шаге обучения
    """
    # Рисуем график ошибки
    # 'b-' - синяя сплошная линия
    # linewidth=2 - толщина линии 2
    plt.plot(errors_list, 'b-', linewidth=2)


def dec_trees_plot_points(dataset, x_col='x_0', y_col='x_1', target_col='y',
                          class_names=('Class 0', 'Class 1'),
                          colors=('blue', 'red'), markers=('s', '^'),
                          title='Классификация точек', xlabel='x0', ylabel='x1',
                          xlim=(0, 10), ylim=(0, 11), figsize=(12, 6), ax=None):
    """
    Визуализирует точки данных из DataFrame с разделением по классам.

    Параметры:
    - dataset: DataFrame с данными
    - x_col: название столбца с данными по оси X
    - y_col: название столбца с данными по оси Y
    - target_col: название столбца с метками классов
    - class_names: подписи классов для легенды
    - colors: цвета для каждого класса
    - markers: маркеры для каждого класса
    - title: заголовок графика
    - xlabel: подпись оси X
    - ylabel: подпись оси Y
    - xlim: пределы оси X
    - ylim: пределы оси Y
    - figsize: размер фигуры (используется только если ax=None)
    - ax: ось matplotlib для отрисовки (если None, создается новая фигура)
    """
    # Разделение данных по меткам
    classes = sorted(dataset[target_col].unique())
    class_data = [dataset[dataset[target_col] == cls] for cls in classes]

    # Создание графика, если не передана ось
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    # Отображение точек для каждого класса
    for i, cls in enumerate(classes):
        ax.scatter(class_data[i][x_col], class_data[i][y_col],
                   marker=markers[i], s=100,
                   label=class_names[i],
                   color=colors[i],
                   edgecolor='black')

    # Настройка осей и заголовка
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.legend()

    # Если создавали новую фигуру, показываем ее
    if ax is None:
        plt.show()

    return ax


def plot_decision_boundary(model, features, labels, title='Decision Boundary',
                           figsize=(8, 6), ax=None, class_names=None,
                           colors=('blue', 'red'), markers=('s', '^')):
    """
    Визуализирует границу решения классификатора.

    Параметры:
    ----------
    model : обученная модель классификатора
    features : DataFrame или массив признаков (X)
    labels : Series или массив меток (y)
    title : str, заголовок графика
    figsize : tuple, размер фигуры (используется только если ax=None)
    ax : ось matplotlib для отрисовки (если None, создается новая фигура)
    class_names : список названий классов
    colors : tuple цветов для классов (должны соответствовать plot_points)
    markers : tuple маркеров для классов (должны соответствовать plot_points)
    """
    # Создание графика, если не передана ось
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    # Проверяем тип features (DataFrame или numpy array)
    if hasattr(features, 'iloc'):  # Если это DataFrame
        x0 = features.iloc[:, 0]
        x1 = features.iloc[:, 1]
    else:  # Если numpy array
        x0 = features[:, 0]
        x1 = features[:, 1]

    # Создаем график границы решения
    DecisionBoundaryDisplay.from_estimator(
        model,
        features,
        response_method="predict",
        plot_method="pcolormesh",
        alpha=0.3,
        cmap='coolwarm',
        ax=ax
    )

    # Получаем уникальные классы в правильном порядке (0, 1, 2...)
    unique_classes = np.unique(labels) if hasattr(labels, 'dtype') else sorted(labels.unique())

    for i, class_label in enumerate(unique_classes):
        mask = (labels == class_label)
        label = f'Class {class_label}' if class_names is None else class_names[i]
        ax.scatter(x0[mask], x1[mask],
                   color=colors[i % len(colors)],
                   marker=markers[i % len(markers)],
                   label=label,
                   edgecolor='black',
                   s=100)

    ax.set_xlabel(features.columns[0] if hasattr(features, 'columns') else 'Feature 1')
    ax.set_ylabel(features.columns[1] if hasattr(features, 'columns') else 'Feature 2')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)

    if ax is None:
        plt.show()

    return ax


# Функция для визуализации границы принятия решений
def nn_plot_function(f, xlim, ylim, happy, sad):
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
