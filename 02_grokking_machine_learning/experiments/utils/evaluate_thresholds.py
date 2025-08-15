# chapter09/utils/evaluate_thresholds.py


import pandas as pd
from .metrics import accuracy, gini_index, entropy, mean_squared_deviation, mean_absolute_deviation


# Генерация порогов по числовому признаку
def generate_thresholds(values):
    """
    Генерирует список пороговых значений для бинарного разделения по числовому признаку.

    Параметры:
        values: Series или список числовых значений (например, df['Возраст'])

    Возвращает:
        Список порогов:
        - Значение меньше минимального (для "всё слева")
        - Все средние точки между уникальными значениями
        - Значение больше максимального (для "всё справа")
    """
    unique_vals = sorted(values.unique())  # Получаем уникальные значения признака и сортируем
    thresholds = []

    if len(unique_vals) > 0:
        thresholds.append(unique_vals[0] - 1)  # Граница слева от минимального значения

        # Добавляем середины между каждым соседним значением
        for i in range(len(unique_vals) - 1):
            mid = (unique_vals[i] + unique_vals[i + 1]) / 2
            thresholds.append(mid)

        thresholds.append(unique_vals[-1] + 1)  # Граница справа от максимального значения

    return thresholds


# Оценка по всем порогам
def evaluate_thresholds(
        df,
        feature_col,
        target_col,
        task='classification',  # 'classification' или 'regression'
        sort_by=None,
        precision=3
):
    """
    Оценивает качество бинарных разделений по числовому признаку на разных порогах
    для задач классификации или регрессии.

    Параметры:
        df: pandas.DataFrame
            Исходные данные с признаками и целевой переменной.
        feature_col: str
            Имя числового признака (столбца), по которому строится разделение.
        target_col: str
            Имя целевого признака (меток классов или числовых значений).
        task: str
            Тип задачи: 'classification' — для классификации, 'regression' — для регрессии.
        sort_by: str или None
            Имя столбца, по которому сортировать результат.
            Если None — сортировка не выполняется.
        precision: int
            Количество знаков после запятой при округлении метрик.

    Возвращает:
        pandas.DataFrame:
            Таблица с результатами по каждому порогу, содержащая:
            - Условие разделения
            - Значения признака в левой и правой группе
            - Метки объектов в обеих группах
            - Метрики качества (в зависимости от задачи)
    """
    # Получаем список всех порогов для признака
    thresholds = generate_thresholds(df[feature_col])
    results = []  # Сюда будем собирать результаты

    # Перебираем каждый порог
    for threshold in thresholds:
        # Делим данные по текущему порогу
        left = df[df[feature_col] < threshold][target_col]  # Левая группа (значения < порога)
        right = df[df[feature_col] >= threshold][target_col]  # Правая группа (значения >= порога)

        # Базовая информация о разбиении
        result = {
            'Вопрос': f'{feature_col} < {threshold:.1f}?',
            'Первый набор (да)': df[df[feature_col] < threshold][feature_col].tolist(),  # значения признака слева
            'Второй набор (нет)': df[df[feature_col] >= threshold][feature_col].tolist(),  # значения признака справа
            'Метки': [left.tolist(), right.tolist()]  # значения целевой переменной в обеих группах
        }

        # Если задача классификации — считаем метрики для категориальных меток
        if task == 'classification':
            groups = [left, right]
            result.update({
                'Взвешенная достоверность': accuracy(groups, precision=precision),
                'Взвешенный индекс примесей Джини': gini_index(groups, precision=precision),
                'Взвешенная энтропия': entropy(groups, precision=precision)
            })

        # Если задача регрессии — считаем MSE и MAE
        elif task == 'regression':
            total_len = len(left) + len(right)  # Общее количество элементов
            weighted_mse = (len(left) * mean_squared_deviation(left) + len(right) * mean_squared_deviation(
                right)) / total_len
            weighted_mae = (len(left) * mean_absolute_deviation(left) + len(right) * mean_absolute_deviation(
                right)) / total_len

            result.update({
                'Взвешенный MSE': round(weighted_mse, precision),
                'Взвешенный MAE': round(weighted_mae, precision)
            })

        # Добавляем результат в общий список
        results.append(result)

    # Преобразуем список словарей в DataFrame
    df_results = pd.DataFrame(results)

    # Если задано поле сортировки и оно есть в DataFrame — сортируем
    if sort_by in df_results.columns:
        df_results = df_results.sort_values(by=sort_by, ascending=True)

    return df_results
