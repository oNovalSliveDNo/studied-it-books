# chapter03/models/linear_regression.py


import random
import numpy as np
from utils.errors import mae, mse, rmse


def simple_trick(base_price, price_per_room, num_rooms, price, learning_rate):
    """
    Простой эвристический способ обновления коэффициентов.
    Он не использует градиент, но корректирует параметры на основе
    того, больше или меньше предсказание фактической цены.

    Параметры:
        base_price (float): Смещение (свободный член).
        price_per_room (float): Вес (цена за одну комнату).
        num_rooms (float): Количество комнат.
        price (float): Реальная цена.
        learning_rate (float): Шаг изменения параметров.

    Возвращает:
        (float, float): Обновлённые значения (price_per_room, base_price).
    """
    small_random_1 = learning_rate
    small_random_2 = learning_rate

    predicted_price = base_price + price_per_room * num_rooms  # предсказание модели

    # Корректировка параметров в зависимости от того, выше или ниже предсказание
    if price > predicted_price and num_rooms > 0:
        price_per_room += small_random_1
        base_price += small_random_2

    if price > predicted_price and num_rooms < 0:
        price_per_room -= small_random_1
        base_price += small_random_2

    if price < predicted_price and num_rooms > 0:
        price_per_room -= small_random_1
        base_price -= small_random_2

    if price < predicted_price and num_rooms < 0:
        price_per_room -= small_random_1
        base_price += small_random_2

    return price_per_room, base_price


def absolute_trick(base_price, price_per_room, num_rooms, price, learning_rate):
    """
    Метод обновления коэффициентов, направленный на минимизацию абсолютной ошибки (MAE).
    Не использует производные, но корректирует веса в нужную сторону.

    Параметры:
        base_price (float): Свободный член (смещение).
        price_per_room (float): Коэффициент при количестве комнат.
        num_rooms (float): Входной признак (кол-во комнат).
        price (float): Целевая переменная (цена).
        learning_rate (float): Скорость обучения.

    Возвращает:
        (float, float): Обновлённые значения (price_per_room, base_price).
    """
    predicted_price = base_price + price_per_room * num_rooms

    if price > predicted_price:
        # Если модель занижает цену — увеличиваем коэффициенты
        price_per_room += learning_rate * num_rooms
        base_price += learning_rate
    else:
        # Если завышает — уменьшаем
        price_per_room -= learning_rate * num_rooms
        base_price -= learning_rate

    return price_per_room, base_price


def square_trick(base_price, price_per_room, num_rooms, price, learning_rate):
    """
    Метод градиентного спуска для минимизации среднеквадратичной ошибки (MSE).

    Параметры:
        base_price (float): Свободный член (смещение).
        price_per_room (float): Вес — цена за одну комнату.
        num_rooms (float): Входной признак (например, количество комнат).
        price (float): Истинная цена (целевая переменная).
        learning_rate (float): Шаг обновления параметров.

    Возвращает:
        (float, float): Обновлённые значения (price_per_room, base_price).
    """
    predicted_price = base_price + price_per_room * num_rooms  # предсказание модели
    error = price - predicted_price  # разница между предсказанием и реальностью

    # Обновляем параметры по направлению антиградиента
    base_price += learning_rate * error  # "сдвигаем" прямую вверх/вниз
    price_per_room += learning_rate * num_rooms * error  # "поворачиваем" прямую

    return price_per_room, base_price


def linear_regression(
        features,  # Входной массив признаков (например, количество комнат)
        labels,  # Целевые значения (например, цены)
        learning_rate=0.01,  # Скорость обучения — насколько сильно обновляются параметры
        epochs=1000,  # Количество итераций обучения
        trick='square',  # Метод обновления весов: 'simple', 'absolute', 'square'
        error='rmse',  # Метрика оценки ошибки: 'mae', 'mse', 'rmse'
        mode='sgd',  # Режим обучения: 'sgd', 'batch', 'mini'
        batch_size=2  # Размер подвыборки (только для режима 'mini')
):
    """
    Обучает линейную модель с помощью различных режимов градиентного спуска и стратегий обновления весов.

    Параметры:
        features (np.ndarray): Массив входных признаков (X).
        labels (np.ndarray): Массив истинных значений (Y).
        learning_rate (float): Шаг градиентного спуска.
        epochs (int): Количество эпох обучения.
        trick (str): Метод обновления весов ('simple', 'absolute', 'square').
        error (str): Метрика ошибки ('mae', 'mse', 'rmse').
        mode (str): Режим градиентного спуска ('sgd', 'batch', 'mini').
        batch_size (int): Размер мини-батча (используется только при mode='mini').

    Возвращает:
        tuple: (price_per_room, base_price, errors_list)
            price_per_room (float): Обученный коэффициент при признаке.
            base_price (float): Обученное смещение.
            errors_list (list): История ошибок на каждой эпохе.
    """
    # Инициализация параметров модели случайными значениями
    price_per_room = random.random()
    base_price = random.random()

    # Список для отслеживания ошибки на каждой итерации
    errors_list = []

    # Словари с доступными функциями обновления весов и метриками
    tricks = {
        'simple': simple_trick,
        'absolute': absolute_trick,
        'square': square_trick
    }

    errors = {
        'mae': mae,
        'mse': mse,
        'rmse': rmse
    }

    # Проверка допустимых значений параметров
    if trick not in tricks:
        raise ValueError("Доступные методы обновления: 'simple', 'absolute', 'square'")

    if error not in errors:
        raise ValueError("Ошибка должна быть одной из: 'mae', 'mse', 'rmse'")

    if mode not in {'sgd', 'batch', 'mini'}:
        raise ValueError("Режим должен быть: 'sgd', 'batch' или 'mini'")

    # Основной цикл обучения
    for epoch in range(epochs):
        # Предсказание по всей выборке
        predictions = price_per_room * features + base_price

        # Сохраняем значение ошибки модели на текущей итерации
        errors_list.append(errors[error](labels, predictions))

        # === Градиентный спуск по выбранному режиму ===
        if mode == 'sgd':
            # SGD: обновление на одной случайной точке
            i = random.randint(0, len(features) - 1)
            x_i, y_i = features[i], labels[i]
            price_per_room, base_price = tricks[trick](
                base_price, price_per_room, x_i, y_i, learning_rate
            )

        elif mode == 'batch':
            # Batch GD: обновление на всех точках (классический режим)
            for x_i, y_i in zip(features, labels):
                predicted = price_per_room * x_i + base_price
                error_i = y_i - predicted
                # Обновляем параметры по градиенту
                base_price += learning_rate * error_i
                price_per_room += learning_rate * x_i * error_i

        elif mode == 'mini':
            # Mini-batch GD: обновление по подмножеству случайных точек
            indices = np.random.choice(len(features), batch_size, replace=False)
            for i in indices:
                x_i, y_i = features[i], labels[i]
                price_per_room, base_price = tricks[trick](
                    base_price, price_per_room, x_i, y_i, learning_rate
                )

    # Возвращаем обученные параметры и историю ошибок
    return price_per_room, base_price, errors_list


def predict(price_per_room, base_price, rooms_count):
    """
    Делает предсказание на основе обученных параметров модели.

    Параметры:
        price_per_room (float): Коэффициент (вес) при количестве комнат.
        base_price (float): Свободный член (смещение).
        rooms_count (float или np.ndarray): Количество комнат (одиночное или массив).

    Возвращает:
        float или np.ndarray: Предсказанная цена.
    """
    return price_per_room * rooms_count + base_price
