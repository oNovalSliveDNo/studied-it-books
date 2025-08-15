# chapter05/models/perceptron_algorithm.py


import random
from utils.errors import perceptron_prediction, mean_perceptron_error


def perceptron_trick(weights, bias, features, label, learning_rate=0.01):
    """
    Реализует один шаг обновления весов и смещения по правилу персептрона.

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
    pred = perceptron_prediction(weights, bias, features)

    for i in range(len(weights)):
        # Обновляем каждый вес в соответствии с правилом персептрона:
        # новый вес = старый вес + (разница между истинной меткой и предсказанием) * признак * скорость обучения
        weights[i] += (label - pred) * features[i] * learning_rate

    # Аналогично обновляем смещение:
    # новое смещение = старое смещение + (разница между истинной меткой и предсказанием) * скорость обучения
    bias += (label - pred) * learning_rate

    return weights, bias


def perceptron_algorithm(features, labels, learning_rate=0.01, epochs=200):
    """
    Реализует алгоритм обучения персептрона.

    Параметры:
        features (list of lists): Матрица признаков (каждый вложенный список - один пример)
        labels (list): Вектор меток классов (0 или 1 для каждого примера)
        learning_rate (float, optional): Скорость обучения. По умолчанию 0.01.
        epochs (int, optional): Количество эпох обучения. По умолчанию 200.

    Возвращает:
        dict: Словарь с результатами обучения, содержащий:
            - final_weights: Финальные веса модели
            - final_bias: Финальное смещение модели
            - errors_history: История ошибок на каждой эпохе
            - weights_history: История весов на каждой эпохе
            - bias_history: История смещений на каждой эпохе
    """
    # Инициализация весов и смещения:
    # Веса инициализируются единицами (можно использовать случайные небольшие числа)
    # Смещение инициализируется нулем
    weights = [1.0 for i in range(len(features[0]))]
    bias = 0.0

    # Инициализация массивов для хранения истории обучения:
    errors_list = []  # Будет хранить ошибку на каждой эпохе
    weights_history = []  # Будет хранить веса на каждой эпохе
    bias_history = []  # Будет хранить смещение на каждой эпохе

    # Основной цикл обучения:
    for epoch in range(epochs):
        # Сохраняем текущие веса и смещение перед обновлением
        # Используем copy(), чтобы избежать ссылочной зависимости
        weights_history.append(weights.copy())
        bias_history.append(bias)

        # Вычисляем среднюю ошибку на текущих весах и сохраняем ее
        error = mean_perceptron_error(weights, bias, features, labels)
        errors_list.append(error)

        # Выбираем случайный пример из обучающего набора для обновления весов
        i = random.randint(0, len(features) - 1)

        # Применяем правило персептрона для обновления весов и смещения
        # на основе выбранного случайного примера
        weights, bias = perceptron_trick(
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
