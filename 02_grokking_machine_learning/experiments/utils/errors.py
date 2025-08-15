# chapter03/utils/errors


import numpy as np


def mae(labels, predictions):
    """MAE — Средняя абсолютная ошибка.

    Шаги:
    1. Вычислить абсолютную разницу между фактическими и предсказанными значениями.
    2. Взять среднее значение этих разниц.
    """
    return np.mean(np.abs(labels - predictions))


def mse(labels, predictions):
    """MSE — Средняя квадратичная ошибка.

    Шаги:
    1. Найти разницу между фактическими и предсказанными значениями.
    2. Возвести эти разницы в квадрат.
    3. Взять среднее значение квадратов ошибок.
    """
    return np.mean((labels - predictions) ** 2)


def rmse(labels, predictions):
    """RMSE — Корень из средней квадратичной ошибки.

    Шаги:
    1. Найти MSE.
    2. Взять квадратный корень из этого значения.
    """
    return np.sqrt(np.mean((labels - predictions) ** 2))


# chapter05/utils/errors.py


def score(weights, bias, features):
    """
    Вычисляет взвешенную сумму признаков (score) (линейную комбинацию) для классификации.

    Параметры:
        weights (numpy.ndarray): Вектор весов модели
        bias (float): Смещение (bias) модели
        features (numpy.ndarray): Вектор признаков одного примера

    Возвращает:
        float: Взвешенная сумма признаков плюс смещение
    """
    # np.dot вычисляет скалярное произведение векторов weights и features
    # к результату добавляется смещение bias
    return np.dot(features, weights) + bias


def step(x):
    """
    Ступенчатая функция активации.

    Параметры:
        x (float): Входное значение

    Возвращает:
        int: 1 если x >= 0, иначе 0
    """
    # Если входное значение x больше или равно 0, возвращаем 1
    if x >= 0:
        return 1
    # Иначе возвращаем 0
    else:
        return 0


def perceptron_prediction(weights, bias, features):
    """
    Выполняет предсказание класса с помощью перцептрона.

    Параметры:
        weights (numpy.ndarray): Вектор весов модели
        bias (float): Смещение (bias) модели
        features (numpy.ndarray): Вектор признаков одного примера

    Возвращает:
        int: Предсказанный класс (0 или 1)
    """
    # Сначала вычисляем score (взвешенную сумму)
    # Затем применяем ступенчатую функцию для получения предсказания
    return step(score(weights, bias, features))


def perceptron_error(weights, bias, features, label):
    """
    Вычисляет ошибку классификации для одного примера.

    Параметры:
        weights (numpy.ndarray): Вектор весов модели
        bias (float): Смещение (bias) модели
        features (numpy.ndarray): Вектор признаков одного примера
        label (int): Истинная метка класса (0 или 1)

    Возвращает:
        float: Ошибка классификации для данного примера
    """
    # Получаем предсказание модели для текущих весов и признаков
    pred = perceptron_prediction(weights, bias, features)

    # Если предсказание совпадает с истинной меткой, ошибка равна 0
    if pred == label:
        return 0

    # Если предсказание неверное, ошибка равна абсолютному значению score
    # Это показывает, насколько "уверенно" модель ошиблась
    else:
        return np.abs(score(weights, bias, features))


def mean_perceptron_error(weights, bias, features, labels):
    """
    Вычисляет среднюю ошибку перцептрона на всем наборе данных.

    Параметры:
        weights (numpy.ndarray): Вектор весов модели
        bias (float): Смещение (bias) модели
        features (numpy.ndarray): Матрица признаков (каждая строка - один пример)
        labels (numpy.ndarray): Вектор истинных меток классов

    Возвращает:
        float: Средняя ошибка перцептрона на всем наборе данных
    """
    # Инициализируем суммарную ошибку
    total_error = 0

    # Проходим по всем примерам в наборе данных
    for i in range(len(features)):
        # Для каждого примера вычисляем ошибку и добавляем к общей сумме
        total_error += perceptron_error(weights, bias, features[i], labels[i])

    # Возвращаем среднюю ошибку (сумма ошибок / количество примеров)
    return total_error / len(features)


def sigmoid(x):
    """
    Вычисляет значение сигмоидной функции.

    Параметры:
        x (float): Входное значение

    Возвращает:
        float: Значение сигмоидной функции в точке x
    """
    # Численно стабильная реализация сигмоиды:
    # Если x >= 0, используем стандартную формулу 1 / (1 + e^(-x))
    if x >= 0:
        return 1 / (1 + np.exp(-x))
    else:
        # Если x < 0, используем эквивалентную форму для избежания переполнения
        return np.exp(x) / (1 + np.exp(x))


def log_reg_prediction(weights, bias, features):
    """
    Выполняет предсказание вероятности положительного класса.

    Параметры:
        weights (numpy.ndarray): Вектор весов модели
        bias (float): Смещение (bias) модели
        features (numpy.ndarray): Вектор признаков одного примера

    Возвращает:
        float: Предсказанная вероятность принадлежности к классу 1
    """
    # Вычисляем score и передаём в сигмоиду для получения вероятности
    return sigmoid(score(weights, bias, features))


def log_loss(weights, bias, features, label):
    """
    Вычисляет логарифмическую потерю (log loss) для одного примера.

    Параметры:
        weights (numpy.ndarray): Вектор весов модели
        bias (float): Смещение (bias) модели
        features (numpy.ndarray): Вектор признаков одного примера
        label (int): Истинная метка класса (0 или 1)

    Возвращает:
        float: Логарифмическая потеря для данного примера
    """
    # Вычисляем предсказанную вероятность
    pred = log_reg_prediction(weights, bias, features)

    # Применяем формулу логарифмической потери:
    # -y * log(p) - (1 - y) * log(1 - p)
    return - label * np.log(pred) - (1 - label) * np.log(1 - pred)


def total_log_loss(weights, bias, features, labels):
    """
    Вычисляет общую логарифмическую потерю по всему набору данных.

    Параметры:
        weights (numpy.ndarray): Вектор весов модели
        bias (float): Смещение (bias) модели
        features (numpy.ndarray): Матрица признаков (каждая строка — один пример)
        labels (numpy.ndarray): Вектор истинных меток классов

    Возвращает:
        float: Суммарная логарифмическая потеря на всем наборе данных
    """
    # Инициализируем суммарную ошибку
    total_error = 0

    # Проходим по всем примерам и накапливаем потери
    for i in range(len(features)):
        total_error += log_loss(weights, bias, features[i], labels[i])

    # Возвращаем суммарную (не усреднённую) логарифмическую потерю
    return total_error
