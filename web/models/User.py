from .Manager import SingletonMeta


class User(metaclass=SingletonMeta):
    def __init__(self):
        self.username = ""
        self.__password = ""
        self.__hashed_password = ""
        self.email = ""
        self.cards = []

    def get_username(self):
        return self.username

    def get_password(self):
        return self.__password

    def get_hashed_password(self):
        return self.__hashed_password

    def get_email(self):
        return self.email

    def get_cards(self):
        return self.cards

    def input_username(self, username):
        self.username = username

    def input_password(self, password):
        self.__password = password

    def input_hashed_password(self, password):
        self.__hashed_password = password

    def input_email(self, email):
        self.email = email

    def update_cards(self, cards):
        self.cards = cards

    def add_card(self, card):
        self.cards.append(card)
