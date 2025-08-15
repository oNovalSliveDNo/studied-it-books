# Блек-джек
# От 1 до 7 игроков против дилера

import cards, games


class BJ_Card(cards.Card):
    """ Карта для игры в Блек-джек. """
    ACE_VALUE = 1  # Значение туза по умолчанию

    @property
    def value(self):
        """ Возвращает значение карты. Для карт с изображениями (J, Q, K) — 10, для туза — 1 или 11. """
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1  # Преобразуем номинал карты в число
            if v > 10:
                v = 10  # Для карт J, Q, K считаем за 10
        else:
            v = None  # Если карта закрыта, значение None
        return v


class BJ_Deck(cards.Deck):
    """ Колода для игры в "Блек-джек". """

    def populate(self):
        """ Заполняет колоду картами для Блек-джека. """
        for suit in BJ_Card.SUITS:  # Для каждой масти
            for rank in BJ_Card.RANKS:  # Для каждого номинала
                self.cards.append(BJ_Card(rank, suit))  # Добавляем карту в колоду


class BJ_Hand(cards.Hand):
    """ 'Рука': набор карт "Блек-джека" у одного игрока. """

    def __init__(self, name):
        """ Инициализация руки с именем игрока. """
        super(BJ_Hand, self).__init__()  # Вызываем конструктор родительского класса (Hand)
        self.name = name  # Имя игрока

    def __str__(self):
        """ Возвращает строковое представление руки игрока с подсчитанным суммарным значением карт. """
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()  # Строковое представление руки
        if self.total:  # Если сумма карт есть
            rep += "(" + str(self.total) + ")"  # Добавляем сумму очков в скобках
        return rep

    @property
    def total(self):
        """ Считает суммарное значение карт на руке, учитывая возможность туза как 1 или 11 очков. """
        for card in self.cards:  # Проверяем все карты на руке
            if not card.value:  # Если у какой-то карты нет значения (закрыта)
                return None  # Возвращаем None

        t = 0
        for card in self.cards:  # Суммируем значения всех карт
            t += card.value

        contains_ace = False
        for card in self.cards:  # Проверяем, есть ли туз
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        # Если есть туз и сумма меньше или равна 11, считаем туз за 11 очков
        if contains_ace and t <= 11:
            t += 10  # Прибавляем 10 (потому что туз уже учтен как 1)

        return t

    def is_busted(self):
        """ Проверка, перебрал ли игрок (сумма очков больше 21). """
        return self.total > 21


class BJ_Player(BJ_Hand):
    """ Игрок в "Блек-джек". """

    def is_hitting(self):
        """ Спрашивает игрока, хочет ли он взять еще карту. """
        response = games.ask_yes_no("\n" + self.name + ", будете брать еще карты? (y/n): ")
        return response == "y"  # Если игрок ответил 'y', возвращаем True

    def bust(self):
        """ Игрок перебрал. """
        print(self.name, "перебрал.")
        self.lose()  # Вызываем метод проигрыша

    def lose(self):
        """ Игрок проиграл. """
        print(self.name, "проиграл.")

    def win(self):
        """ Игрок выиграл. """
        print(self.name, "выиграл.")

    def push(self):
        """ Ничья с дилером. """
        print(self.name, "сыграл с компьютером вничью.")


class BJ_Dealer(BJ_Hand):
    """ Дилер в игре "Блек-джек". """

    def is_hitting(self):
        """ Дилер берет карту, если его сумма меньше 17. """
        return self.total < 17

    def bust(self):
        """ Дилер перебрал. """
        print(self.name, "перебрал.")

    def flip_first_card(self):
        """ Переворачивает первую карту дилера (начальная карта должна быть скрыта). """
        first_card = self.cards[0]  # Берем первую карту
        first_card.flip()  # Переворачиваем карту


class BJ_Game(object):
    """ Игра в Блек-джек. """

    def __init__(self, names):
        """ Инициализация игры. Создаем игроков, дилера и колоду. """
        self.players = []  # Список игроков
        for name in names:  # Для каждого имени создаем игрока
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Dealer")  # Создаем дилера

        self.deck = BJ_Deck()  # Создаем колоду
        self.deck.populate()  # Заполняем колоду картами
        self.deck.shuffle()  # Перемешиваем колоду

    @property
    def still_playing(self):
        """ Возвращает список игроков, которые не перебрали (которые еще могут продолжить игру). """
        sp = []  # Список игроков, которые еще не перебрали
        for player in self.players:
            if not player.is_busted():  # Если игрок не перебрал, добавляем его в список
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        """ Сдает дополнительные карты игроку, пока тот не перебрал или не решил остановиться. """
        while not player.is_busted() and player.is_hitting():  # Пока игрок не перебрал и хочет взять карту
            self.deck.deal([player])  # Сдаем карту игроку
            print(player)  # Показываем карты игрока
            if player.is_busted():  # Если игрок перебрал, вызываем его перебор
                player.bust()

    def play(self):
        """ Основной игровой процесс. """
        # Сдача всем по 2 карты, включая дилера
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # Переворачиваем первую карту дилера, чтобы она была скрыта
        for player in self.players:
            print(player)  # Показываем карты каждого игрока
        print(self.dealer)  # Показываем карты дилера (первая скрыта)

        # Сдача дополнительных карт игрокам
        for player in self.players:
            self.__additional_cards(player)  # Вызываем функцию для сдачи дополнительных карт

        self.dealer.flip_first_card()  # Теперь открываем первую карту дилера

        if not self.still_playing:
            # Если все игроки перебрали, показываем только "руку" дилера
            print(self.dealer)
        else:
            # Если есть игроки, продолжаем игру, сдавая карты дилеру
            print(self.dealer)
            self.__additional_cards(self.dealer)  # Сдаем карты дилеру

            if self.dealer.is_busted():
                # Если дилер перебрал, выигрывают все игроки, которые остались в игре
                for player in self.still_playing:
                    player.win()
            else:
                # Если дилер не перебрал, сравниваем суммы очков у игроков и дилера
                for player in self.still_playing:
                    if player.total > self.dealer.total:  # Если игрок выиграл
                        player.win()
                    elif player.total < self.dealer.total:  # Если игрок проиграл
                        player.lose()
                    else:  # Если ничья
                        player.push()

        # После завершения игры очищаем все карты у игроков и дилера
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    """ Главная функция игры. """
    print("\t\tДoбpo пожаловать за игровой стол Блек-джека!\n")

    names = []  # Список имен игроков
    number = games.ask_number("Cкoлькo всего игроков? (1 - 7): ", low=1, high=8)  # Спрашиваем количество игроков
    for i in range(number):  # Запрашиваем имена игроков
        name = input("Введите имя игрока: ")
        names.append(name)
    print()

    game = BJ_Game(names)  # Создаем игру с данными игроками

    again = None
    while again != "n":
        game.play()  # Запускаем игру
        again = games.ask_yes_no("\nXoтитe сыграть еще раз? (y/n): ")  # Спрашиваем, хотят ли сыграть снова


# Запуск игры
main()
input("\n\nНажмите Enter, чтобы выйти.")
