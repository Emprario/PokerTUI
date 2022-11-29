class CardValueError(Exception):
    """The Value must be an integer between 2 and 14 (Ace)"""

    def __init__(self, expression):
        pass


class CardColorError(Exception):
    """The Color must be a string in french : 'Coeur', 'Carreau', 'Trèfle', 'Pique')"""

    def __init__(self, expression):
        pass


class CardFigureError(Exception):
    """The Figure must be a string in english : 2 to 10 and 'Ace','King','Queen','Jocker'"""

    def __init__(self, expression):
        pass


class FigureComparaisonError(Exception):
    """The figure you want to compare is just impossible to have on two examples"""

    def __init__(self, expression):
        pass

class Impossible42Error(Exception):
    """Crongratulation maybe ?"""

    def __init__(self, expresion):
        pass
