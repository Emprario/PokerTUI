from poker import Poker
from carte import Carte
from player import Player
from ui import UI
from random import shuffle
from errors import Impossible42Error


class Croupier():
    """User Logic Interface (between the user, UI and Poker)"""
    maxmoney = 99_999

    def __init__(self):
        self.__poker = Poker()
        self.__ui = UI(False)
        self.deck = None
        self.cid = 0
        self.players = dict()
        self.Table = []
        self.order = (self.__get_flop, self.__get_tour, self.__get_river)
        self.pot = 0
        self.activeid = 0
        self.states = ("Actif", "Couché", "Focus", "ATapis", "Out")
        self.iddealer = 0
        self.idblind_small = 0
        self.idblind_big = 0
        self.small_blind = 5

    def set_small_blind(self,blind:int):
        self.small_blind = blind

    def get_deck(self):
        return self.deck

    def gen_deck(self):
        self.deck = [
            Carte(v, c) for v in range(2, 15, 1)
            for c in ['Carreau', 'Coeur', 'Pique', 'Trèfle']
        ]

    def shuffle_deck(self):
        shuffle(self.deck)

    def drop_card(self) -> object:
        return self.deck.pop(-1)

    def print_deck(self, adeck=None):  # By default it's self.deck
        if adeck == None:
            adeck = self.deck
        print('[', end="")
        if adeck != None:
            for carte in adeck:
                print(carte, end=", ")
        else:
            print("None", end="  ")
        print("\b\b]")

    def add_player(self,name) -> int:
        self.cid += 1
        self.players[self.cid] = Player(name)
        return self.cid

    def get_last_player_id(self) -> int:
        return self.cid

    def del_player(self, id: int):
        del self.players[id]

    def distribute(self):
        for playerkey in self.players:
            self.players[playerkey].cards = [
                self.drop_card(), self.drop_card()
            ]

    def __get_flop(self):
        return [self.drop_card() for i in range(3)]

    def __get_tour(self):
        return [self.drop_card()]

    def __get_river(self):
        return [self.drop_card()]

    def get_onTable(self):
        return self.Table

    def add_onTable(self):
        for i in range(len(self.order)):
            self.Table += self.order[i]()
            yield self.get_onTable()

    def reg_money(self, player_id: int, money: int):
        self.players[player_id].money = money

    def get_money(self, player_id: int) -> int:
        return self.players[player_id].money

    def get_active_playername(self) -> str:
        return self.players[self.activeid].name

    def get_player_state(self, playerid: int) -> int:
        if self.players[playerid].out:
            return 4
        elif self.players[playerid].iscouche:
            return 1
        elif playerid == self.players[playerid].atapis:
            return 3
        elif playerid == self.activeid:
            return 2
        else:
            return 0

    def print_players_state(self):
        #  ■  @@nickname@  ■  #   □  @nickname  □   #
        #   Money : XXXXX µ   #
        #   State : Actif     # | Couché | Focus
        #   Mise  : XXXXX µ   #
        for playerid in self.players:
            activestate_id = self.get_player_state(playerid)
            nickname = list("  □  ##########  □  ")
            money = list("   Money: XXXXX µ   ")
            state = list("   State : SSSSSS   ")
            mise = list("   Mise : XXXXX µ   ")

            ## Nickname
            i = 0
            for char in self.players[playerid].name:
                nickname[5 + i] = char
                i += 1
            for j in range(i, 10):
                nickname[5 + j] = " "

            if activestate_id == 2:
                nickname[2] = "■"
                nickname[17] = "■"
            elif activestate_id == 1:
                nickname[2] = "X"
                nickname[17] = "X"
            elif activestate_id == 3:
                nickname[2] = "#"
                nickname[17] = "#"
            elif activestate_id == 4:
                nickname[2] = " "
                nickname[17] = " "

            ##money
            i = 0
            moneystr = str(self.players[playerid].money)
            for char in moneystr:
                money[10 + i] = char
                i += 1
            for j in range(i, 5):
                money[10 + j] = " "

            ## State
            i = 0
            player_state = self.states[activestate_id]
            for char in player_state:
                state[11 + i] = char
                i += 1
            for j in range(i, 6):
                state[11 + j] = " "

            ## mise
            i = 0
            misestr = str(self.players[playerid].mise)
            for char in misestr:
                mise[10 + i] = char
                i += 1
            for j in range(i, 5):
                mise[10 + j] = " "

            self.__ui.vpara("".join(nickname) + "\n" + "".join(money) + "\n" +
                            "".join(state) + "\n" + "".join(mise))
        self.__ui.flush(self.__ui.vpara)

    def print_private_header(self):
        self.__ui.vseparation()
        self.__ui.vprint("\t\tPrivate Space (Not visibal by other players)\n",
                         end=True)

    def print_public_header(self):
        self.__ui.vseparation()
        self.__ui.vprint("\tPublic Space (Visibal by other players)\n",
                         end=True)

    def print_public_info(self):
        self.__ui.vprint(f"Dans le pot : {self.pot}", end=True)

    def print_private_info(self, playerid):
        #TODO: print les cartes
        self.__ui.vprint(f"In Bank : {self.players[playerid].money}\n")
        self.__ui.vprint(
            f"Votre mise actuelle : {self.players[playerid].mise}")
        self.__ui.flush(self.__ui.vprint)

    def ask_addmise(self, playerid, min):
        if self.players[playerid].iscouche or self.players[playerid].atapis:
            self.__ui.vprint(
                "Vous ne pouvez pas jouer ce tour ci. Soit vous vous êtes couché soit parti à tapis",
                True)
            return
        while True:
            add = self.__ui.vinput("Combien voulez-vous misez ? ")
            action = "miser"
            try:
                if add in ("se coucher", "coucher", "abandonne", "STOP",
                           "stop"):
                    action = "se coucher"
                elif add in ("TAPIS", "tapis", "tapi"):
                    action = "tapis"
                else:
                    action = "miser"
                    add = int(add)
                    assert add == min or add >= 2 * min
            except:
                self.__ui.vprint(
                    f"Veuillez rentrez un nombre entier naturel égale à la mise minimale pour suivre : {min}\n"
                )
                self.__ui.vprint(
                    f"Vous pouvez également relancer avec une somme supérieur ou égale au double de la mise maximale : {min*2}\n"
                )
                self.__ui.vprint(
                    "Vous pouvez également vous coucher en tapant 'se coucher'"
                )
                self.__ui.flush(self.__ui.vprint)
            else:
                if action == "miser":
                    if self.players[playerid].money < add:
                        self.__ui.vprint(
                            "Vous ne pouvez miser que ce que vous avez ou alors tapez 'tapis' pour partir à tapis",
                            end=True)
                        continue
                    self.__miser(playerid, add)
                elif action == "se coucher":
                    self.__se_coucher(playerid)
                elif action == "tapis":
                    self.__tapis(playerid)
                else:
                    raise Impossible42Error("Croupier.ask_addmise")
                break

    def __miser(self, playerid, mise):
        self.players[playerid].money -= mise
        self.players[playerid].mise = mise

    def __se_coucher(self, playerid):
        self.players[playerid].iscouche = True

    def __tapis(self, playerid):
        self.players[playerid].atapis = True
        self.players[playerid].mise = self.players[playerid].money
        self.players[playerid].money = 0

    def set_pot(self):
        """Every player affected"""
        for playerid in self.players:
            self.pot += self.players[playerid].mise
            self.players[playerid].mise = 0

    def set_isoff(self, playerid, kick=False):
        if self.players[playerid].money == 0:
            if kick:
                self.kick_player(playerid)
            else:
                self.players[playerid].out = True
                self.__ui.vprint(
                    f"{self.players[playerid].name} n'a plus d'argent il est out !",
                    True)

    def kick_player(self, playerid):
        x = self.players[playerid]
        del self.players[playerid]
        self.__ui.vprint(f"{x.name} a été kick !", True)

    def transaction(self, playerid):
        self.__ui.vprint(
            f" Transaction de {self.pot} vers {self.players[playerid].name}",
            True)
        self.players[playerid].money += self.pot
        self.pot = 0

    def thebestplayer(self):
        playerenjeu = [
            playerid for playerid in self.players
            if not self.players[playerid].iscouche
            and not self.players[playerid].out
        ]
        bestplayer = playerenjeu[0]
        for i in range(playerenjeu):
            x = self.__poker.the_best(self.get_onTable(), 
 bestplayer.cards, playerenjeu[i].cards)
            if x == True:
                continue
            elif x == False:
                bestplayer = playerenjeu[i]
            elif x == None:
                continue
        return bestplayer
