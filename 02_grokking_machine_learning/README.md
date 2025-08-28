# 🤖 Grokking Machine Learning — конспекты и эксперименты

Коллекция конспектов, практических заданий и моих экспериментов по книге **"Grokking Machine Learning"** (Luis Serrano).
Репозиторий структурирован по главам книги и содержит как объяснения, так и практические реализации алгоритмов машинного обучения.

> 🧠 Проект создан как шаг к глубокому пониманию основ ML: от линейной регрессии до ансамблей моделей.

---

## 📂 Оглавление README.md

* [📖 Описание репозитория](#-описание-репозитория)
* [📚 О книге](#-о-книге)
* [🎯 Цель репозитория](#-цель-репозитория)
* [💾 Установка](#-установка)
* [📂 Структура проекта](#-структура-проекта)
* [🚀 Как запускать примеры](#-как-запускать-примеры)
* [📚 Темы по главам](#-темы-по-главам)
* [🔔 Примечания](#-примечания)
* [✅ Тестирование](#-тестирование)
* [📚 Полезные ресурсы](#-полезные-ресурсы)
* [📝 Лицензия](#-лицензия)

---

## 📖 Описание репозитория

Этот репозиторий — результат моего обучения по книге **"Grokking Machine Learning"**.

* 💡 Все ключевые алгоритмы реализованы "с нуля" на Python.
* 📊 Каждая глава сопровождается **Jupyter Notebook**, где пошагово показаны эксперименты и визуализации.
* ⚙️ В папке `models/` находятся собственные реализации алгоритмов.
* 🎨 В папке `utils/` собраны вспомогательные функции для графиков, метрик и отчётности.

---

## 📚 О книге

* **Автор:** Luis Serrano
* **Название:** *Grokking Machine Learning*
* **Фокус:** интуитивное введение в машинное обучение через простые объяснения, визуализации и практику.

> Цель книги — объяснить основы ML так, чтобы они стали понятны "изнутри", без сухой теории и перегрузки формулами.

---

## 🎯 Цель репозитория

* 🧠 Освоить фундаментальные алгоритмы ML.
* 📝 Систематизировать конспекты и практику по главам.
* 🔬 Показывать работу моделей через наглядные примеры.
* 📂 Создать удобную структуру для повторения и будущего использования.

---

## 💾 Установка

### 1. Установите Python 3.13.3

Рекомендуемая версия: **Python 3.13.3**.
Проверка версии:

```bash
python --version
```

### 2. Клонируйте репозиторий

```bash
git clone https://github.com/oNovalSliveDNo/studied-it-books.git
```

### 3. Установите зависимости

```bash
cd studied-it-books/02_grokking_machine_learning
pip install -r requirements.txt
```

### 4. Используйте виртуальное окружение (опционально)

```bash
python -m venv env
source env/bin/activate  # macOS/Linux
.\env\Scripts\activate   # Windows
```

---

## 📂 Структура проекта

```markdown
02_grokking_machine_learning
├── README.md              # Подробное описание проекта
├── experiments/           # Jupyter Notebook'и по главам
│   ├── 01_what_is_machine_learning.ipynb
│   ├── 02_types_of_machine_learning.ipynb
│   ├── ...
│   ├── 13_end2end_project.ipynb
│   ├── data/              # Датасеты
│   │   ├── titanic.csv
│   │   ├── IMDB_Dataset.csv
│   │   ├── ...
│   │   └── pictures/      # Схемы и иллюстрации
│   ├── models/            # Реализации алгоритмов
│   │   ├── linear_regression.py
│   │   ├── logistic_regression_algorithm.py
│   │   ├── perceptron_algorithm.py
│   │   └── polynomial_regression.py
│   └── utils/             # Вспомогательные функции
│       ├── metrics.py
│       ├── plot_points.py
│       ├── plot_decision_boundary.py
│       └── ...
├── knowledge_map.drawio   # Карта знаний
└── requirements.txt       # Зависимости проекта
```

---

## 🚀 Как запускать примеры

1. Запустите **Jupyter Lab** или **Jupyter Notebook**:

```bash
jupyter lab
```

2. Откройте нужную тетрадку в папке `experiments/`.
3. Выполните ячейки по порядку.
4. Альтернатива — запуск в IDE (VS Code, PyCharm).

---

## 📚 Темы по главам

| Глава | Тетрадь                                             | Тема                     | Краткое описание                           |
| ----- | --------------------------------------------------- | ------------------------ | ------------------------------------------ |
| 1     | 01\_what\_is\_machine\_learning.ipynb               | Что такое ML?            | Основные понятия и интуиция.               |
| 2     | 02\_types\_of\_machine\_learning.ipynb              | Виды ML                  | Supervised, Unsupervised, Reinforcement.   |
| 3     | 03\_linear\_regression.ipynb                        | Линейная регрессия       | Реализация и визуализация.                 |
| 4     | 04\_underfitting\_and\_overfitting.ipynb            | Пере- и недообучение     | Примеры, графики.                          |
| 5     | 05\_perceptron\_algorithm.ipynb                     | Алгоритм перцептрона     | Классика бинарной классификации.           |
| 6a    | 06a\_logistic\_regression\_algorithm.ipynb          | Логистическая регрессия  | Реализация с нуля.                         |
| 6b    | 06b\_classification\_of\_movie\_reviews\_imdb.ipynb | IMDb Sentiment Analysis  | Работа с реальным текстовым датасетом.     |
| 7     | 07\_evaluation\_of\_classification\_models.ipynb    | Метрики классификации    | Accuracy, Precision, Recall, F1, ROC.      |
| 8     | 08\_naive\_bayes.ipynb                              | Наивный Байес            | Вероятностный классификатор.               |
| 9     | 09\_decision\_trees.ipynb                           | Деревья решений          | Пошаговое построение.                      |
| 10    | 10\_neural\_networks.ipynb                          | Нейронные сети           | Введение и простая реализация.             |
| 11    | 11\_support\_vector\_machines.ipynb                 | SVM                      | Метод опорных векторов.                    |
| 12a   | 12a\_classification\_ensemble\_methods.ipynb        | Ансамбли (классификация) | Bagging, Boosting, Voting.                 |
| 12b   | 12b\_regression\_ensemble\_methods.ipynb            | Ансамбли (регрессия)     | Random Forest и Gradient Boosting.         |
| 13    | 13\_end2end\_project.ipynb                          | End-to-End проект        | Комплексный кейс с обработкой данных и ML. |

---

## 🔔 Примечания

* Все примеры протестированы на **Python 3.13.3**.
* Некоторые датасеты (`IMDB_Dataset.csv`, `Titanic.csv`) взяты из открытых источников.
* Код адаптирован под современные библиотеки (`numpy`, `pandas`, `scikit-learn`, `matplotlib`).

---

## ✅ Тестирование

Автоматических тестов нет.
Каждая тетрадка проверялась вручную: все алгоритмы и визуализации работают.

---

## 📚 Полезные ресурсы

* [Документация Python](https://docs.python.org/3/)
* [Scikit-learn](https://scikit-learn.org/stable/)
* [TensorFlow](https://www.tensorflow.org/)
* [Keras](https://keras.io/)

---

## 📝 Лицензия

Проект распространяется под лицензией **MIT**.
Подробнее см. файл [LICENSE](../LICENSE).
