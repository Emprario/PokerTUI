#from carte import Carte
#from croupier import Croupier
#from ui import UI
from game import Game
#from createcards import create_cards


def jeu2test():
    # Carte(0, "Carreau")
    # Carte(1, "Red")
    carte = Carte(12, "Trèfle")
    print(carte)

    poker = Croupier()
    lst = [
        Carte(4, "Trèfle"),
        Carte(12, "Pique"),
        Carte(10, "Coeur"),
        Carte(12, "Carreau"),
        Carte(11, "Carreau")
    ]
    #lstbis = [
    #    Carte(14, "Coeur"),
    #    Carte(14, "Carreau"),
    #    Carte(10, "Coeur"),
    #    Carte(12, "Trèfle"),
    #    Carte(10, "Coeur")
    #]
    A = [Carte(10, "Trèfle"), Carte(4, "Coeur")]
    B = [Carte(6, "Carreau"), Carte(10, "Pique")]
    TableA = [('4', 'Trèfle'), ('Queen', 'Pique'), ('10', 'Coeur'),
              ('Queen', 'Carreau'), ('10', 'Trèfle')]
    TableB = [('4', 'Trèfle'), ('Queen', 'Pique'), ('10', 'Coeur'),
              ('Queen', 'Carreau'), ('10', 'Pique')]

    poker.gen_deck()
    poker.shuffle_deck()
    #poker.print_deck()
    TableA = poker.convert_figurecouleur2card(TableA)
    TableB = poker.convert_figurecouleur2card(TableB)
    print(poker.best_hauteur(TableA, TableB))
    print(poker.the_best(lst, A, B))


def jeu2test2():
    TUI = UI()
    TUI.vimage("assets/cmi/carreau9.cmi", end=False)
    TUI.vimage("assets/cmi/coeurJ.cmi", end=False)
    TUI.vimage("assets/cmi/carreau10.cmi", end=True)
    TUI.vimage("assets/cmi/trefle1.cmi", end=False)
    TUI.vimage("assets/cmi/piqueK.cmi", end=False)
    TUI.flush(TUI.vimage)

    croupier = Croupier()
    croupier.print_public_header()
    croupier.gen_deck()
    croupier.shuffle_deck()
    Aid = croupier.add_player()
    Bid = croupier.add_player()
    croupier.distribute()
    #for Table in croupier.add_onTable():
    #    croupier.print_deck(Table)
    #croupier.print_deck(list(croupier.players[Aid].cards))
    #croupier.print_deck(list(croupier.players[Bid].cards))
    croupier.print_players_state()
    croupier.print_private_header()
    croupier.print_public_info()
    croupier.print_private_info(Aid)
    croupier.ask_addmise(1, 10)


if __name__ == "__main__":
    #create_cards()
    Game()
