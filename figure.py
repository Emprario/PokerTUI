from errors import FigureComparaisonError


class Figure:

    def sq_as_values(fct):

        def inner(self, *args):
            tmp = [*args]
            for i in range(len(tmp)):
                tmp[i] = [c.get_valeur() for c in tmp[i]]
            return fct(self, *tmp)

        return inner

    def sq_as_couleur(fct):

        def inner(self, *args):
            tmp = [*args]
            for i in range(len(tmp)):
                tmp[i] = [c.get_couleur() for c in tmp[i]]
            return fct(self, *tmp)

        return inner

    ### Les Figures (Comparation entre 5 Carte) ###

    ## Présence
    ## is_figure(s: séquence de 5 carte) -> bool:

    def is_hauteur(self, s):
        return True  # Toujours OUI

    @sq_as_values
    def is_paire(self, s):
        for i in range(0, 5):
            tmp = s[:i] + s[i + 1:]
            if s[i] in tmp:
                return True
        return False

    @sq_as_values
    def is_dpaire(self, s):
        paire = 0
        for i in range(0, 5):
            tmp = s[:i] + s[i + 1:]
            if s[i] in tmp:
                paire += 1
        if paire >= 4:  # Car 1 paire réelle = 2paire
            return True
        else:
            return False

    @sq_as_values
    def is_brelan(self, s):
        for i in range(0, 5):
            bre = 0
            for j in range(0, 5):
                if s[i] == s[j]:
                    bre += 1
            if bre >= 3:
                return True
        return False

    @sq_as_values
    def is_suite(self, s):
        s.sort()
        if s[0] > s[1]:
            crois = -1
        else:
            crois = 1
        for i in range(1, 5):
            if s[0] + (i * crois) != s[i]:
                return False
        return True

    @sq_as_couleur
    def is_couleur(self, s):
        for i in range(1, 5):
            if s[0] != s[i]:
                return False
        return True

    @sq_as_values
    def is_full(self, s):
        paire = None
        for i in range(0, 5):  # cherche la paire
            for j in range(0, 5):
                if i != j and s[i] == s[j]:
                    paire = s[i]
                    break
        if paire == None:
            return False
        hist = dict()
        for i in range(0, 5):  # Cherche le brelan
            for j in range(0, 5):
                if s[i] == s[j]:
                    if not (s[i] in hist):
                        hist[s[i]] = 0
                    hist[s[i]] += 1
        for v in hist.values():
            if v >= 9 and v != paire:  # Met au carré le nb de carte
                return True
        return False

    @sq_as_values
    def is_carre(self, s):
        for i in range(0, 5):
            car = 0
            for j in range(0, 5):
                if s[i] == s[j]:
                    car += 1
            if car >= 4:
                return True
        return False

    def is_quinteflush(self, s):
        return self.is_couleur(s) and self.is_suite(s)

    def is_quinteflush_royale(self, s):
        return self.is_quinteflush(s) and (14 in [c.get_valeur() for c in s])

    ## Comparaison
    ## best_figure(A: séquence de 5 cartes,B: séquence de 5 cartes) -> bool or None (True = A, False = B, None = Egalité):

    @sq_as_values
    def best_hauteur(self, A, B):
        camp = None
        maxA = max(*A)
        maxB = max(*B)
        if maxA == maxB:
            return None
        else:
            return maxA > maxB

        return camp

    def __best_paire_one(self, A, cond):
        for i in range(0, 5):  # cherche la paire
            for j in range(0, 5):
                if cond(A, i, j):
                    paire = A[i]
                    break
        return paire

    @sq_as_values
    def best_paire(self, A, B):
        paireA = self.__best_paire_one(A,
                                       lambda s, i, j: i != j and s[i] == s[j])
        paireB = self.__best_paire_one(B,
                                       lambda s, i, j: i != j and s[i] == s[j])
        if paireA == paireB:
            return None
        return paireA > paireB

    @sq_as_values
    def best_dpaire(self, A, B):
        paireA = [None, None]
        paireA[0] = self.__best_paire_one(
            A, lambda s, i, j: i != j and s[i] == s[j])
        paireA[1] = self.__best_paire_one(
            A, lambda s, i, j: i != j and s[i] == s[j] and s[i] != paireA[0])
        paireAmax = max(paireA[0], paireA[1])
        paireAmin = min(paireA[0], paireA[1])
        paireB = [None, None]
        paireB[0] = self.__best_paire_one(
            B, lambda s, i, j: i != j and s[i] == s[j])
        paireB[1] = self.__best_paire_one(
            B, lambda s, i, j: i != j and s[i] == s[j] and s[i] != paireB[0])
        paireBmax = max(paireB[0], paireB[1])
        paireBmin = min(paireB[0], paireB[1])
        if paireAmax == paireBmax:
            if paireAmin == paireBmin:
                return None
            return paireAmin > paireBmin
        return paireAmax > paireBmax

    def __best_maxcarte_one(self, A, count):
        for i in range(0, 5):
            bre = 0
            max = 0
            for j in range(0, 5):
                if A[i] == A[j]:
                    bre += 1
                    max = A[i]
            if bre >= count:
                return max

    @sq_as_values
    def best_brelan(self, A, B):
        a = self.__best_maxcarte_one(A, 3)
        b = self.__best_maxcarte_one(B, 3)
        if a == b:
            return None
        return a > b

    def __best_suite_one(self, A):
        A.sort()
        if A[0] > A[1]:
            crois = -1
        else:
            crois = 0
        return A[crois]

    @sq_as_values
    def best_suite(self, A, B):
        a = self.__best_suite_one(A)
        b = self.__best_suite_one(B)
        if a == b:
            return None
        return a > b

    def best_couleur(self, A, B):
        return self.best_hauteur(A, B)  # Revient à

    @sq_as_values
    def best_full(self, A, B):
        a = self.__best_maxcarte_one(A, 3)
        b = self.__best_maxcarte_one(B, 3)
        if a != b:
            return a > b
        a = self.__best_paire_one(
            A, lambda s, i, j: i != j and s[i] == s[j] and s[i] != a)
        b = self.__best_paire_one(
            B, lambda s, i, j: i != j and s[i] == s[j] and s[i] != b)
        if a == b:
            return None
        return a > b

    @sq_as_values
    def best_carre(self, A, B):
        a = self.__best_maxcarte_one(A, 4)
        b = self.__best_maxcarte_one(B, 4)
        if a == b:
            return None
        return a > b

    def best_quinteflush(self, A, B):
        return self.best_suite(A, B)

    def best_quinteflush_royale(self, A, B):
        raise FigureComparaisonError(A, B)
