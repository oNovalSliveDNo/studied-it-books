# Прочитаем
# Демонстрирует чтение из текстового файла

print("Открываю и закрываю файл.")
# Открываем файл для чтения (r) с кодировкой UTF-8
text_file = open("read_it.txt", "r", encoding='utf-8')
# Закрываем файл после открытия (на данный момент ничего не читаем)
text_file.close()

print("\nЧитaю файл посимвольно.")
# Открываем файл для чтения посимвольно
text_file = open("read_it.txt", "r", encoding='utf-8')
# Читаем один символ из файла
print(text_file.read(1))
# Читаем следующие 5 символов
print(text_file.read(5))
# Закрываем файл
text_file.close()

print("\nЧитaю файл целиком.")
# Открываем файл для чтения целиком
text_file = open("read_it.txt", "r", encoding='utf-8')
# Читаем весь файл в одну строку
whole_thing = text_file.read()
# Печатаем весь текст файла
print(whole_thing)
# Закрываем файл
text_file.close()

print("\nЧитaю одну строку посимвольно.")
# Открываем файл для чтения
text_file = open("read_it.txt", "r", encoding='utf-8')
# Читаем одну строку, но по одному символу
print(text_file.readline(1))
# Читаем еще 5 символов из этой строки
print(text_file.readline(5))
# Закрываем файл
text_file.close()

print("\nЧитaю одну строку целиком.")
# Открываем файл для чтения
text_file = open("read_it.txt", "r", encoding='utf-8')
# Читаем одну строку целиком
print(text_file.readline())
# Читаем следующую строку
print(text_file.readline())
# Читаем еще одну строку
print(text_file.readline())
# Закрываем файл
text_file.close()

print("\nЧитaю весь файл в список.")
# Открываем файл для чтения
text_file = open("read_it.txt", "r", encoding='utf-8')
# Читаем все строки из файла и сохраняем их в список
lines = text_file.readlines()
# Печатаем все строки в списке
print(lines)
# Печатаем количество строк в файле
print(len(lines))
# Печатаем каждую строку из списка
for line in lines:
    print(line)
# Закрываем файл
text_file.close()

print("\nПepeбиpaю файл построчно.")
# Открываем файл для чтения
text_file = open("read_it.txt", "r", encoding='utf-8')
# Читаем файл построчно и выводим каждую строку
for line in text_file:
    print(line)
# Закрываем файл
text_file.close()

# Ожидаем от пользователя нажатия Enter перед выходом
input("\n\nHaжмитe Enter, чтобы выйти.")
