from crouier import Croupier
from ui import UI

class Game():
    """Classe gérant le jeu et le réseau (WIP)"""

    def __init__(self,auto = True):
        self.croupier = Croupier()
        self.__ui = UI(True)
        self.blind = 0
        self.auto = auto
        if self.auto:
            self.init_game_local()

    def init_game_local(self):
        while self.__ui.input("Ajouter un joueur ? [o/n]") == "o":
            self.croupier.add_player(self.__ui.input("Nom [Pas d'espace et max 10 caractères] : "))
            self.__ui.vprint(f"Bienvenue {self.croupier.players[get_last_player_id()].name}")
        while True:
            x = self.__ui.vinput("Small blind de départ ? ")
            try:
                x = int(x)
                assert x > 0
                self.croupier.set_small_blind(x)
                break
            except:
                self.__ui.vprint("La blind doit être supérieur strict à 0")
        self.__ui.vprint("Configuration terminée")
        if self.auto:
            self.loop()

    def tour2game(self):
        pass

    def loop(self):
        pass