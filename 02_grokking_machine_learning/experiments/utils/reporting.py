# chapter03/utils/reporting.py


import numpy as np
from models.polynomial_regression import predict_polynomial


def format_equation(slope, intercept, precision=2):
    """
    Форматирует уравнение прямой вида y = mx + b.

    Parameters:
        slope (float): Наклон прямой.
        intercept (float): Смещение (свободный член).
        precision (int): Количество знаков после запятой.

    Returns:
        str: Строковое представление уравнения.
    """
    m = round(slope, precision)  # Округляем наклон до нужной точности
    b = round(intercept, precision)  # Округляем смещение до нужной точности
    sign = "+" if b >= 0 else "-"  # Выбираем знак между m*x и b
    # Возвращаем строку вида: y = 2.0 * x + 5.0
    return f"y = {m} * x {sign} {abs(b)}"


def print_prediction(slope, intercept, x_value):
    """
    Формирует строку с предсказанием для линейной модели.

    Parameters:
        slope (float): Наклон прямой.
        intercept (float): Свободный член.
        x_value (float or int): Значение x, для которого делается прогноз.

    Returns:
        str: Строка с результатом предсказания.
    """
    y = slope * x_value + intercept  # Вычисляем предсказанное значение
    return f"Для {x_value} комнат → Предсказанная цена: {y:.2f}"


def format_polynomial_equation(weights, precision=2):
    """
    Форматирует уравнение полинома по заданным весам.

    Параметры:
    weights (list): Список коэффициентов полинома, где индекс элемента
                    соответствует степени переменной x.
    precision (int): Количество знаков после запятой для округления коэффициентов.

    Возвращает:
    str: Строка, представляющая полиномиальное уравнение в формате:
         y = w0 + (w1 * x^1) + (w2 * x^2) + ... + (wn * x^n)
    """

    # Создаем список для хранения форматированных термов полинома
    terms = []

    # Перебираем все коэффициенты вместе с их индексами
    for i, w in enumerate(weights):
        # Округляем коэффициент до указанной точности
        rounded_w = round(w, precision)

        # Форматируем терм в зависимости от степени x:
        if i == 0:
            # Свободный член (x^0) выводим без указания переменной
            term = f"{rounded_w}"
        else:
            # Для остальных коэффициентов создаем терм вида (w * x^i)
            term = f"({rounded_w} * x^{i})"

        # Добавляем отформатированный терм в список
        terms.append(term)

    # Объединяем все термы через ' + ' и добавляем префикс 'y = '
    return "y = " + " + ".join(terms)


def print_prediction_poly(weights, degree, x_value, precision=2):
    """
    Делает предсказание и форматирует его для полиномиальной регрессии.

    Parameters:
        weights (np.ndarray): Коэффициенты полинома.
        degree (int): Степень полинома.
        x_value (float or int): Значение x, для которого делается прогноз.
        precision (int): Кол-во знаков после запятой для результата.

    Returns:
        str: Строка с результатом предсказания.
    """
    # Вызываем функцию предсказания, подаём x как массив из одного элемента
    y_pred = predict_polynomial(weights, np.array([x_value]), degree)[0]
    # Возвращаем красиво отформатированный результат
    return f"Для x = {x_value} → Предсказанное значение: {y_pred:.{precision}f}"


def print_weights(weights, bias, feature_names, decision=2):
    """
    Выводит на экран веса модели и смещение в удобном формате.

    Параметры:
        weights (list или numpy.ndarray): Вектор весов модели
        bias (float): Значение смещения (bias) модели
        feature_names (list): Список названий признаков
        decision (int, optional): Количество знаков после запятой для округления. По умолчанию 2.

    Возвращает:
        None: Функция только выводит информацию на экран
    """
    # Создаем строку формата для вывода чисел с заданной точностью
    # Например, при decision=2 получим формат "{:.2f}"
    format_str = f"{{:.{decision}f}}"

    # Проходим по всем признакам и их весам одновременно
    # zip объединяет элементы из feature_names и weights попарно
    for name, weight in zip(feature_names, weights):

        # Форматируем вес признака в строку с заданным количеством знаков после запятой
        weight_str = format_str.format(weight)

        # Для положительных весов добавляем пробел перед числом для выравнивания
        # Это нужно потому, что у отрицательных чисел есть знак "-", который занимает место
        if weight >= 0:
            # Выводим вес с дополнительным пробелом перед положительным числом
            # \t - символ табуляции для выравнивания
            print(f'Вес «{name.lower()}»:\t {weight_str}')

        else:
            # Для отрицательных весов пробел не добавляем, так как знак "-" уже занимает место
            print(f'Вес «{name.lower()}»:\t{weight_str}')

    # Форматируем и выводим смещение (bias)
    bias_str = format_str.format(bias)

    # Выводим смещение с табуляцией для выравнивания с другими строками
    print(f'Смещение:\t{bias_str}')
