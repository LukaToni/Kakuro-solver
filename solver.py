import numpy as np
import collections
import itertools


def get_right_number_filed(i, j, length_game):
    num = 0
    for right_field in range(j, length_game):
        if isinstance(game[i][right_field], tuple):
            break
        else:
            num = num + 1
    return num


def get_down_number_filed(i, j, high_game):
    num = 0
    for down_field in range(i, high_game):
        if isinstance(game[down_field][j], tuple):
            break
        else:
            num = num + 1
    return num


def check_duplicate_number(np_array):
    collected = collections.Counter(np_array)
    for i in collected:
        if collected[i] > 1:
            print("Duplicate")
            return -1
    return 0


def st_ele_gor_dol(length_game, high_game, game):
    for i in range(0, length_game):
        for j in range(0, high_game):
            ele = game[i][j]
            if isinstance(ele, tuple):
                down_num = 0
                right_num = 0

                down = ele[0]
                if down != 0:
                    # get number of filed for insert numbers
                    down_num = get_down_number_filed(i + 1, j, high_game)

                right = ele[1]
                if right != 0:
                    # get number of filed for insert numbers
                    right_num = get_right_number_filed(i, j + 1, length_game)
            else:
                game[i][j] = ele


def ni_duplikatov(vrednosti):
    mnozica = set(vrednosti)
    if len(mnozica) == len(vrednosti):
        return True
    return False


def mozne_kombinacije(st_polj, sestevek):
    rez = set()
    all_possible_num = []
    numbers = [1,2,3,4,5,6,7,8,9]
    # dobiš vse pare kombinacij za dano vsoto in podano število polj
    for seq in itertools.combinations(numbers, st_polj):
        if sum(seq) == sestevek:
            rez.add(seq)
    return rez


def mozna_stevila(st_polj, sestevek):
    all_possible_num = []
    numbers = [1,2,3,4,5,6,7,8,9]
    # dobiš vse pare kombinacij za dano vsoto in podano število polj
    for seq in itertools.combinations(numbers, st_polj):
        if sum(seq) == sestevek:
            for num in seq:
                all_possible_num.append(num)

    all_nums = np.unique(np.array(all_possible_num))
    #return rez
    return set(all_nums)


def algoritem(game, len, high):
    # algoritem based on: http://amit.metodi.me/oldcode/java/kakuro.php
    # poisci kje se vpisuje vrednosti in dodeli mozne vrednosti polju
    mnozice = [[set() for _ in range(len)] for _ in range(high)]

    # pogledamo mozne kandidate za vsa polja navzdol - STEP 1
    for i in range(0, len):
        for j in range(0, high):
            ele = game[i][j]
            if isinstance(ele, tuple):
                down = ele[0]
                if down != 0:
                    # get number of filed for insert numbers
                    down_num = get_down_number_filed(i + 1, j, high-1)
                    mozna = mozna_stevila(down_num, down)
                    # sedaj vsem dol dodelimo mozne vrednosti (STEP 1 za navpicne)
                    # dao +1 in -1 da je bolj jasno kaj se dogaja
                    for k in range(i+1, i+down_num):
                        for m in mozna:
                            mnozice[k][j].add(m)

    # sedaj pogledamo se za kandidate desno, poleg tega pa naredimo presek vseh, da izlocimo neverjetne - STEP 1 & 2
    for i in range(0, len):
        for j in range(0, high):
            ele = game[i][j]
            if isinstance(ele, tuple):
                right = ele[1]
                if right != 0:
                    # get number of filed for insert numbers
                    right_num = get_right_number_filed(i, j + 1, length_game-1)
                    mozna = mozna_stevila(right_num, right)
                    # sedaj naredimo tmp in v polja mnozice shranimo presek med vodoravnimi/navpicnimi vrednostmmi (STEP 2)
                    for k in range(j+1, j+right_num):
                        tmp = set()
                        for m in mozna:
                            tmp.add(m)
                        mnozice[i][k] = mnozice[i][k].intersection(tmp)

    # sedaj smo naredili korak 2 -> imamo torej informirano mrezo, ki nam pove mozne stevilke v posametnem polju.
    # tukaj lahko izberemo en informiran algoritem in uporabimo mrezo mnozice. lotimo se koraka 3 (STEP 3)
    #TODO v 132 vrstici je napaka
    for i in range(0, len):
        for j in range(0, high):
            # ce je mozna le ena stevilka jo vpisemo v igro
            if len(mnozice[i][j]) == 1:
                game[i][j] = list(mnozice[i][j])[0]

    return mnozice
    # STEP 4


if __name__ == "__main__":
    set_of_number = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    kakuro_1_N = [[(0, 0), (23, 0), (30, 0), (0, 0), (0, 0), (27, 0), (12, 0), (16, 0)],
                  [(0, 16), 0, 0, (0, 0), (17, 24), 0, 0, 0],
                  [(0, 17), 0, 0, (15, 29), 0, 0, 0, 0],
                  [(0, 35), 0, 0, 0, 0, 0, (12, 0), (0, 0)],
                  [(0, 0), (0, 7), 0, 0, (7, 8), 0, 0, (7, 0)],
                  [(0, 0), (11, 0), (10, 16), 0, 0, 0, 0, 0],
                  [(0, 21), 0, 0, 0, 0, (0, 5), 0, 0],
                  [(0, 6), 0, 0, 0, (0, 0), (0, 3), 0, 0]]
    np_kakuro_1_N = np.array(kakuro_1_N)

    kakuro_1_S = [[(0, 0), (23, 0), (30, 0), (0, 0), (0, 0), (27, 0), (12, 0), (16, 0)],
                  [(0, 16), 9, 7, (0, 0), (17, 24), 8, 7, 9],
                  [(0, 17), 8, 9, (15, 29), 8, 9, 5, 7],
                  [(0, 35), 6, 8, 5, 9, 7, (12, 0), (0, 0)],
                  [(0, 0), (0, 7), 6, 1, (7, 8), 2, 6, (7, 0)],
                  [(0, 0), (11, 0), (10, 16), 4, 6, 1, 3, 2],
                  [(0, 21), 8, 9, 3, 1, (0, 5), 1, 4],
                  [(0, 6), 3, 1, 2, (0, 0), (0, 3), 2, 1]]

    np_kakuro_1_S = np.array(kakuro_1_S)
    game = np_kakuro_1_N

    length_game = len(game)

    high_game = len(game[0])

    down_num = 0
    right_num = 0
    #print(mozna_stevila(4, 13))
    #print(mozne_kombinacije(4, 13))
    mn = algoritem(game, length_game, high_game)
    for m in mn:
        print(m)
