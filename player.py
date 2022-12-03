from random import choice


class Player:

    def __init__(self, money, name: str = None):
        self.cards = []  # Erease everything each time you modify cards
        self.money = money
        self.mise = 0
        if name == "" or name == None or len(
                name.split()) != 1 or len(name) > 10:
            name = f"player-{choice([i for i in range(100,1000)])}"
        self.name = name
        self.iscouche = False
        self.atapis = False
        self.out = False
