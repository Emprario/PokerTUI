from errors import CardValueError, CardColorError, CardFigureError


class Carte:

    def __init__(self, var: int, couleur: str = ""):
        if var == "fake":
            self.fake = True
        else:
            self.fake = False
        self.figure = ["Jocker", "Queen", "King", "Ace"
                       ] + [str(i) for i in range(2, 11)]
        self.figure_complex = {
            11: "Jocker",
            12: "Queen",
            13: "King",
            14: "Ace"
        }
        self.figure_complex_figurekey = {
            "Jocker": 11,
            "Queen": 12,
            "King": 13,
            "Ace": 14
        }
        self.colors = ['Carreau', 'Coeur', 'Pique', 'Trèfle']
        if not self.fake:
            self.__is_CardValueError(var)
            self.set_valeur(var)

            self.is_CardColorError(couleur)
            self.set_couleur(couleur)

    def __is_CardValueError(self, x: int):
        if type(x) != int or x < 2 or x > 14:
            raise CardValueError(x)

    def is_CardColorError(self, c: str):
        if type(c) != str or (c not in self.colors):
            raise CardColorError(c)

    def is_CardFigureError(self, c: str):
        if type(c) != str or (c not in self.figure):
            raise CardFigureError(c)

    def get_valeur(self):
        return self.valeur

    def get_couleur(self):
        return self.couleur

    def get_figure(self):
        return self.figure

    def set_valeur(self, x: int):
        self.__is_CardValueError(x)
        self.valeur = x
        self.__set_figure(x)

    def set_couleur(self, c):
        self.is_CardColorError(c)
        self.couleur = c

    def __set_figure(self, x: int):
        deck = {11: "Jocker", 12: "Queen", 13: "King", 14: "Ace"}
        if self.valeur > 10:
            self.figure = deck[self.valeur]
        else:
            self.figure = str(self.valeur)

    def __str__(self):
        return str((self.get_figure(), self.get_couleur()))

