# chapter06/models/logistic_regression_algorithm.py

import random
from utils.errors import log_reg_prediction, total_log_loss


def logistic_trick(weights, bias, features, label, learning_rate=0.01):
    """
    Реализует один шаг обновления весов и смещения для логистической регрессии
    с использованием стохастического градиентного спуска.

    Параметры:
        weights (list): Текущие веса модели
        bias (float): Текущее смещение модели
        features (list): Входные признаки одного примера
        label (int): Истинная метка класса (0 или 1)
        learning_rate (float, optional): Скорость обучения. По умолчанию 0.01.

    Возвращает:
        tuple: Обновленные веса и смещение
    """
    # Получаем предсказание модели для данного примера
    pred = log_reg_prediction(weights, bias, features)

    for i in range(len(weights)):
        # Обновляем каждый вес по формуле градиентного спуска:
        # новый вес = старый вес + скорость обучения * (истинная метка - предсказание) * значение признака
        weights[i] += learning_rate * (label - pred) * features[i]

    # Обновляем смещение по аналогичной формуле:
    # новое смещение = старое смещение + скорость обучения * (истинная метка - предсказание)
    bias += learning_rate * (label - pred)

    return weights, bias


def logistic_regression_algorithm(features, labels, learning_rate=0.01, epochs=1000):
    """
    Реализует обучение логистической регрессии с использованием стохастического
    градиентного спуска.

    Параметры:
        features (list of lists): Матрица признаков (каждый вложенный список — один пример)
        labels (list): Вектор меток классов (0 или 1 для каждого примера)
        learning_rate (float, optional): Скорость обучения. По умолчанию 0.01.
        epochs (int, optional): Количество эпох обучения. По умолчанию 1000.

    Возвращает:
        dict: Словарь с результатами обучения, содержащий:
            - final_weights: Финальные веса модели
            - final_bias: Финальное смещение модели
            - errors_history: История ошибок (логарифмическая потеря) на каждой эпохе
            - weights_history: История весов на каждой эпохе
            - bias_history: История смещений на каждой эпохе
    """
    # Инициализация весов и смещения:
    # Веса инициализируются единицами (можно использовать случайные небольшие числа)
    # Смещение инициализируется нулем
    weights = [1.0 for i in range(len(features[0]))]
    bias = 0.0

    # Инициализация массивов для хранения истории обучения:
    errors_list = []  # Будет хранить логарифмическую ошибку на каждой эпохе
    weights_history = []  # Будет хранить веса на каждой эпохе
    bias_history = []  # Будет хранить смещение на каждой эпохе

    # Основной цикл обучения:
    for epoch in range(epochs):
        # Сохраняем текущие веса и смещение перед обновлением
        # Используем copy(), чтобы избежать ссылочной зависимости
        weights_history.append(weights.copy())
        bias_history.append(bias)

        # Вычисляем логарифмическую потерю на текущих весах и сохраняем ее
        errors_list.append(total_log_loss(weights, bias, features, labels))

        # Выбираем случайный пример из обучающего набора для обновления весов
        i = random.randint(0, len(features) - 1)

        # Применяем стохастический градиентный шаг для обновления весов и смещения
        weights, bias = logistic_trick(
            weights, bias, features[i], labels[i], learning_rate
        )

    # Возвращаем результаты обучения в виде словаря
    return {
        'final_weights': weights,  # Финальные веса модели
        'final_bias': bias,  # Финальное смещение модели
        'errors_history': errors_list,  # История ошибок
        'weights_history': weights_history,  # История весов
        'bias_history': bias_history  # История смещений
    }
