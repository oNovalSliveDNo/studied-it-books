from fractions import Fraction  # класс Fraction из fractions для работы с дробями
import numpy as np
import math


def decimal_to_fraction(decimal_num, tolerance=1e-9):
    """
    Преобразует десятичную дробь в обыкновенную.

    Параметры:
    - decimal_num: float - десятичное число для преобразования
    - tolerance: float - точность для определения периодичности (по умолчанию 1e-9)

    Возвращает:
    - Fraction object - обыкновенная дробь
    """

    if np.isnan(decimal_num):
        return 0

    else:
        # Разделяем число на целую и дробную части:
        # integer_part - целая часть числа (получается через приведение к int)
        integer_part = int(decimal_num)

        # fractional_part - дробная часть (исходное число минус целая часть)
        fractional_part = decimal_num - integer_part

        # Если дробная часть очень мала (меньше заданной точности),
        # значит число практически целое, возвращаем его как дробь
        if abs(fractional_part) < tolerance:
            return Fraction(integer_part)

        # Пробуем разные длины периода (от 1 до 9 цифр)
        for period_length in range(1, 10):

            # Вычисляем множитель как 10 в степени длины периода
            multiplier = 10 ** period_length

            # "Сдвигаем" число на период влево (умножаем на 10^period_length)
            shifted_num = decimal_num * multiplier

            # Вычисляем разницу между сдвинутым и исходным числом
            difference = shifted_num - decimal_num

            # Проверяем, является ли разница практически целым числом
            # (с учетом заданной точности tolerance)
            if abs(round(difference) - difference) < tolerance:
                # Знаменатель дроби будет 10^period_length - 1
                denominator = multiplier - 1

                # Числитель - округленная разница
                numerator = round(difference)

                # Находим наибольший общий делитель (НОД) для упрощения дроби
                common_divisor = math.gcd(numerator, denominator)

                # Упрощаем числитель
                simplified_num = numerator // common_divisor

                # Упрощаем знаменатель
                simplified_den = denominator // common_divisor

                # Учитываем целую часть в числителе:
                # total_numerator = целая_часть * знаменатель + числитель
                total_numerator = integer_part * simplified_den + simplified_num

                # Возвращаем дробь с новым числителем и знаменателем
                return Fraction(total_numerator, simplified_den)

        # Если не удалось найти период (число не периодическое),
        # используем стандартное преобразование Fraction с ограничением знаменателя
        return Fraction(decimal_num).limit_denominator()
