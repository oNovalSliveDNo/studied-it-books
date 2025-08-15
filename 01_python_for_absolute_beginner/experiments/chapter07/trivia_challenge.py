# Викторина
# Игра на выбор правильного варианта ответа,
# вопросы которой читаются из текстового файла

import sys


# Функция для открытия файла
def open_file(file_name, mode):
    """Открывает файл."""
    try:
        # Пытаемся открыть файл с указанным именем и режимом
        the_file = open(file_name, mode, encoding='utf-8')
    except IOError as e:
        # Если файл не открылся (например, не существует), выводим ошибку
        print("Невозможно открыть файл", file_name, "Работа программы будет завершена.\n", e)
        input("\n\nHaжмитe Enter, чтобы выйти.")
        sys.exit()  # Завершаем программу
    else:
        # Если файл открылся успешно, возвращаем объект файла
        return the_file


# Функция для чтения строки из файла
def next_line(the_file):
    """Возвращает в отформатированном виде очередную строку игрового файла."""
    # Читаем строку
    line = the_file.readline()
    # Заменяем символы '/' на символ новой строки для форматирования
    line = line.replace("/", "\n")
    return line


# Функция для чтения одного блока данных из файла
def next_block(the_file):
    """Возвращает очередной блок данных из игрового файла."""
    # Читаем категории, вопрос, ответы, правильный ответ и объяснение
    category = next_line(the_file)
    question = next_line(the_file)

    # Считываем все ответы
    answers = []
    for i in range(4):
        answers.append(next_line(the_file))

    # Читаем правильный ответ
    correct = next_line(the_file)
    if correct:
        correct = correct[0]  # Берем первый символ как правильный ответ

    # Читаем объяснение к вопросу
    explanation = next_line(the_file)

    # Возвращаем все данные блока
    return category, question, answers, correct, explanation


# Функция для приветствия игрока
def welcome(title):
    """Приветствует игрока и сообщает тему игры."""
    print("\t\tДoбро пожаловать в игру 'Викторина'!\n")
    print("\t\t", title, "\n")


# Основная функция игры
def main():
    # Открываем файл с вопросами викторины
    trivia_file = open_file("trivia.txt", "r")
    # Читаем заголовок викторины
    title = next_line(trivia_file)
    # Приветствуем игрока
    welcome(title)
    score = 0  # Инициализируем счет

    # Извлекаем первый блок данных (категория, вопрос, ответы и т.д.)
    category, question, answers, correct, explanation = next_block(trivia_file)
    while category:
        # Выводим на экран категорию и вопрос
        print(category)
        print(question)

        # Выводим возможные варианты ответов
        for i in range(4):
            print("\t", i + 1, "-", answers[i])

        # Получаем ответ от игрока
        answer = input("Baш ответ: ")

        # Проверяем ответ игрока
        if answer == correct:
            print("\nДа!", end=" ")  # Если ответ правильный
            score += 1  # Увеличиваем счет
        else:
            print("\nНет.", end=" ")  # Если ответ неправильный
        print(explanation)  # Выводим объяснение

        # Выводим текущий счет
        print("Cчeт:", score, "\n\n")

        # Переходим к следующему вопросу
        category, question, answers, correct, explanation = next_block(trivia_file)

    # Закрываем файл после завершения игры
    trivia_file.close()

    # Выводим финальный результат
    print("Этo был последний вопрос!")
    print("Ha вашем счету", score)


# Запуск игры
main()

# Ожидаем от игрока нажатия Enter перед выходом
input("\n\nHaжмите Enter, чтобы выйти.")
