from croupier import Croupier
from ui import UI


class Game():
    """Classe gérant le jeu et le réseau (WIP)"""

    def __init__(self, auto=True):
        self.croupier = Croupier()
        self.__ui = UI(True)
        self.blind = 0
        self.auto = auto
        self.winner = 0
        self.gfirstboth = True
        if self.auto:
            self.init_game_local()

    def init_game_local(self):
        while True:
            x = self.__ui.vinput("Somme de départ ? ")
            try:
                x = int(x)
                assert x > 0
                self.croupier.set_base_money(x)
                break
            except:
                self.__ui.vprint("La somme de base doit être supérieur strict à 0")

        while self.__ui.vinput(
                "Ajouter un joueur ? [o/n]"
        ) == "o" or self.croupier.get_nbplayers_notout() < 2:
            self.croupier.add_player(
                self.__ui.vinput("Nom [Pas d'espace et max 10 caractères] : "))
            self.__ui.vprint(
                f"Bienvenue {self.croupier.players[self.croupier.get_last_player_id()].name}"
            )

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
        firstboth = True and self.gfirstboth
        kill = False
        self.winner = 0
        while not kill:
            for key in self.croupier.next_player():
                self.print_whole_table(key)
                if self.croupier.is_alone_couche():
                    kill = True
                    self.winner = self.croupier.get_winner()
                elif self.equal(self.croupier.get_mises()) and not firstboth:
                    kill = True
                elif self.croupier.is_alone_atapis() and not firstboth:
                    kill = True
                    self.gfirstboth = False
                else:
                    # Check if the player can play:
                    self.croupier.ask_addmise(key, max(self.croupier.get_mises()))
                    #print(self.croupier.get_name(key))
                    self.__ui.vinput(
                            "Pressez 'entrer' pour passer au joueur suivant")
                self.__ui.clear()
            firstboth = False
        self.croupier.set_pot()

    def print_whole_table(self, playerid):
        self.croupier.print_public_header()
        self.croupier.print_cards()
        self.croupier.print_players_state()
        self.croupier.print_private_header()
        self.croupier.print_public_info()
        self.croupier.print_private_info(playerid)

    def loop(self):
        while self.croupier.get_nbplayers_notout() > 1:
            self.croupier.rolling_pieces()
            self.croupier.set_blinds()
            self.croupier.gen_deck()
            self.croupier.shuffle_deck()
            self.croupier.distribute()
            self.__ui.vinput(
                "Le jeu va commencer, le jeu du joueur 1 va être afficher"
            )  # Brute input pour cacher les cartes
            self.__ui.clear()
            for table in self.croupier.add_onTable():
                self.tour2game()
                self.__ui.vinput("Passer au tour suivant")
                self.__ui.clear()
                if self.winner != 0:
                    self.win_manche(self.winner)
                    break
            else:
                self.win_manche(self.croupier.thebestplayer(),True)

        self.croupier.win()
        if self.auto:
            self.kill()

    def win_manche(self,id,show = False):
        if show:
            self.__ui.vprint(f"Jeu du gagnant ({self.croupier.get_name(id)}) :")
            self.print_whole_table(id)
        self.croupier.transaction(id)
        self.croupier.set_isoff()
        self.croupier.clear_data()

    def kill(self):
        self.__ui.vinput("Confirmer la sortie du programme ...")
        del self.croupier
        del self
        exit(0)

    def equal(self, lst):
        for i in range(1, len(lst)):
            if lst[i - 1] != lst[i]:
                return False
        return True
