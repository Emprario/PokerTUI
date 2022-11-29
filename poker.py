from figure import Figure
from carte import Carte


class Poker(Figure):
    """Logical class only, not intented for the end user"""
    from random import shuffle

    def __init__(self):
        self.combos = {
            #int_decrease:[nickname,fct2search,fct2compare]
            9: [
                "Quinte Flush Royale", self.is_quinteflush_royale,
                self.best_quinteflush_royale
            ],
            8: ["Quinte Flush", self.is_quinteflush, self.best_quinteflush],
            7: ["Carré", self.is_carre, self.best_carre],
            6: ["Full", self.is_full, self.best_couleur],
            5: ["Couleur", self.is_couleur, self.best_couleur],
            4: ["Suite", self.is_suite, self.best_suite],
            3: ["Brelan", self.is_brelan, self.best_brelan],
            2: ["Double Paire", self.is_dpaire, self.best_dpaire],
            1: ["Paire", self.is_paire, self.best_paire],
            0: ["Hauteur", self.is_hauteur, self.best_hauteur]
        }
        dist = [  # Grab from dcode/combinaison
            1, 2, 3, 4, 5, 1, 2, 3, 4, 6, 1, 2, 3, 4, 7, 1, 2, 3, 5, 6, 1, 2,
            3, 5, 7, 1, 2, 3, 6, 7, 1, 2, 4, 5, 6, 1, 2, 4, 5, 7, 1, 2, 4, 6,
            7, 1, 2, 5, 6, 7, 1, 3, 4, 5, 6, 1, 3, 4, 5, 7, 1, 3, 4, 6, 7, 1,
            3, 5, 6, 7, 1, 4, 5, 6, 7, 2, 3, 4, 5, 6, 2, 3, 4, 5, 7, 2, 3, 4,
            6, 7, 2, 3, 5, 6, 7, 2, 4, 5, 6, 7, 3, 4, 5, 6, 7
        ]
        self.dist = [[dist[i] - 1 for i in range(start, start + 5)]
                     for start in range(0, len(dist), 5)]
        self.fake = Carte("fake")

    def __best_2xfive(
        self, A: list, B: list
    ) -> [
            True or None, ...
    ]:  # (True = A, False = B, None = Egalité) and return the int of the power of combo
        """Choose the best combinaison of 2 pack of 5 cards"""
        for key in self.combos:
            find = []
            for C in [A, B]:
                if self.combos[key][1](C):
                    find.append(C)
            if len(find) == 2:
                best = self.combos[key][2](A, B)
                if best != None:
                    return best, key
                else:
                    return None, -1
            elif len(find) == 1:
                if find[0] == A:
                    return True, key
                else:
                    return False, key
        return None, -1  # Egalité

    def the_best(
            self, Table: list, A: list,
            B: list) -> bool or None:  # (True = A, False = B, None = Egalité)
        """Choose the best combinaison of 2 pack of 2 cards and the Table (5 cards)"""
        TableA = [C for C in self.__next_comb(Table + A)]
        TableB = [C for C in self.__next_comb(Table + B)]
        bestcomboA = None
        bestcomboB = None
        memoniac = []
        for ta in TableA:
            for tb in TableB:
                x = self.__best_2xfive(ta, tb)
                memoniac.append((ta, tb, x))
                if x[0] == None:
                    continue
                elif (x[0] and bestcomboA == None) or (x[0]
                                                       and bestcomboA < x[1]):
                    bestcomboA = x[1]
                elif (not x[0]
                      and bestcomboB == None) or (not x[0]
                                                  and bestcomboB < x[1]):
                    bestcomboB = x[1]
        if bestcomboA == bestcomboB:
            # Cherche le meilleur A/B
            bestAB = []
            memoniac = [log for log in memoniac if log[2][1] == bestcomboA
                        ]  #Garde uniquement en mémoire les games de ce combo
            memoAB = [[log[0] for log in memoniac],
                      [log[1] for log in memoniac]]

            for iC in range(2):
                maxjeu = memoAB[iC][0]
                for tC in memoAB[iC]:
                    if self.__best_2xfive(tC, maxjeu)[0]:
                        maxjeu = tC
                bestAB.append(maxjeu)
            x = self.__best_2xfive(bestAB[0], bestAB[1])[0]
            if x == None:
                return None
            else:
                return x

        elif bestcomboA > bestcomboB:
            return True
        else:
            return False

    def __next_comb(self, A):
        for comb in self.dist:
            yield [A[comb[i]] for i in range(5)]

    def convert_figurecouleur2card(self, A: list):
        converted = []
        for fcard in A:
            self.fake.is_CardFigureError(fcard[0])
            self.fake.is_CardColorError(fcard[1])
            if fcard[0] in self.fake.figure_complex.values():
                key = self.fake.figure_complex_figurekey[fcard[0]]
            else:
                key = int(fcard[0])
            converted.append(Carte(key, fcard[1]))
        return converted