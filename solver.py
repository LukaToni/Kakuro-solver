import numpy as np
import collections
import itertools
from itertools import permutations
import backtracing
import time
from pandas import *


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

# first init alg
def algoritem_init(game, length, high):
    # algoritem based on: http://amit.metodi.me/oldcode/java/kakuro.php
    # poisci kje se vpisuje vrednosti in dodeli mozne vrednosti polju
    mnozice = [[set() for _ in range(length)] for _ in range(high)]

    # pogledamo mozne kandidate za vsa polja navzdol - STEP 1
    for i in range(0, length):
        for j in range(0, high):
            ele = game[i][j]
            if isinstance(ele, tuple):
                down = ele[0]
                mnozice[i][j] = ([], [])
                if down != 0:
                    # get number of filed for insert numbers
                    down_num = get_down_number_filed(i + 1, j, high)
                    mozna = mozna_stevila(down_num, down)
                    # najdemo mozne kombinacije
                    mnozice[i][j][0].append(mozne_kombinacije(down_num, down))
                    # sedaj vsem dol dodelimo mozne vrednosti (STEP 1 za navpicne)
                    for k in range(i+1, i+down_num+1):
                        for m in mozna:
                            mnozice[k][j].add(m)

    # sedaj pogledamo se za kandidate desno, poleg tega pa naredimo presek vseh, da izlocimo neverjetne - STEP 1 & 2
    for i in range(0, length):
        for j in range(0, high):
            ele = game[i][j]
            if isinstance(ele, tuple):
                right = ele[1]
                if right != 0:
                    # get number of filed for insert numbers
                    right_num = get_right_number_filed(i, j + 1, length_game)
                    mozna = mozna_stevila(right_num, right)
                    # najdemo mozne kombinacije
                    mnozice[i][j][1].append(mozne_kombinacije(right_num, right))
                    # sedaj naredimo tmp in v polja mnozice shranimo presek med vodoravnimi/navpicnimi vrednostmmi (STEP 2)
                    for k in range(j+1, j+right_num+1):
                        tmp = set()
                        for m in mozna:
                            tmp.add(m)
                        mnozice[i][k] = mnozice[i][k].intersection(tmp)

    # stPolj nam pove koliko polj moramo rešiti
    stPolj = 0
    stResenih = 0
    for i in range(0, length):
        for j in range(0, high):
            if not isinstance(game[i][j], tuple):
                stPolj += 1
                # ce je mozna le ena stevilka jo vpisemo v igro
                if len(mnozice[i][j]) == 1:
                    stResenih += 1
                    game[i][j] = list(mnozice[i][j])[0]

    return mnozice, stPolj, stResenih

def algoritem_solve(game, length, high, mnozice):
    for i in range(0, length):
        for j in range(0, high):
            ele = game[i][j]
            if isinstance(ele, tuple):
                # down je sum, down_num je pa st polj za resit
                down = ele[0]
                if down != 0:
                    # get number of filed for insert numbers
                    down_num = get_down_number_filed(i + 1, j, high)
                    resena_stevila = set()
                    # pogledamo katera sevila so ze resena
                    for k in range(i + 1, i + down_num + 1):
                        if len(mnozice[k][j]) == 1:
                            resena_stevila.add(list(mnozice[k][j])[0])
                    # ce imamo se neresena polja
                    if len(resena_stevila) != down_num:
                        new_down = down - sum(resena_stevila)
                        new_down_num = down_num - len(resena_stevila)
                        nova_mozna_st = mozna_stevila(new_down_num, new_down)
                        nova_mozna_st = nova_mozna_st.difference(resena_stevila)
                        # posodobimo mrezo
                        for k in range(i + 1, i + down_num + 1):
                            #TODO preverjanje kombinacij; preveri kaj tocno naredi to kar si spisal
                            if len(mnozice[k][j]) != 1:
                                mnozice[k][j] = mnozice[k][j].intersection(nova_mozna_st)
                        # preverimo ce so kaksne kombinacije odvec in odstranimo odvecne
                        test = mnozice[i][j]
                        if len(mnozice[i][j][0][0]) > 1:
                            odstrani = []
                            for k in range(i + 1, i + down_num + 1):
                                for m in mnozice[i][j][0][0]:
                                    if len(set(m).intersection(mnozice[k][j])) == 0:
                                        odstrani.append(m)
                            # ce smo nasli odvecne, se jih znebimo
                            if len(odstrani) != 0:
                                for o in odstrani:
                                    # preverjamo, ker ga lahko po nesreci veckrat odstranimo
                                    if o in mnozice[i][j][0][0]:
                                        mnozice[i][j][0][0].remove(o)
                                tmp = set()
                                for m in mnozice[i][j][0][0]:
                                    tmp = tmp.union(m)
                                for k in range(i + 1, i + down_num + 1):
                                    mnozice[k][j] = mnozice[k][j].intersection(tmp)
                        # sedaj pogledamo če lahko kaj generiramo
                        kombinacije = mnozice[i][j][0][0]
                        stev = []
                        nove_stev = []
                        for k in range(i + 1, i + down_num + 1):
                            stev.append(mnozice[k][j])
                            nove_stev.append(set())
                        odstrani = []
                        for ko in kombinacije:
                            perm_komb = list(permutations(ko))
                            # preverimo ce je permutacija ok
                            ok_kombinacija = False
                            for p in perm_komb:
                                # preverimo ce je iteracija permutacije ok
                                ok_iteracija = True
                                for ix, s in enumerate(stev):
                                    if len(s.intersection({p[ix]})) == 0:
                                        ok_iteracija = False
                                if ok_iteracija == True:
                                    ok_kombinacija = True
                                    for ix in range(len(nove_stev)):
                                        nove_stev[ix] = nove_stev[ix].union({p[ix]})
                            if ok_kombinacija == False:
                                odstrani.append(ko)
                        for o in odstrani:
                            if o in mnozice[i][j][0][0]:
                                mnozice[i][j][0][0].remove(o)
                        for k, nov in enumerate(nove_stev):
                            mnozice[i+k+1][j] = nov

    for i in range(0, length):
        for j in range(0, high):
            ele = game[i][j]
            if isinstance(ele, tuple):
                right = ele[1]
                if right != 0:
                    # get number of filed for insert numbers
                    right_num = get_right_number_filed(i, j + 1, length_game)
                    resena_stevila = set()
                    # pogledamo katera sevila so ze resena
                    for k in range(j + 1, j + right_num + 1):
                        if len(mnozice[i][k]) == 1:
                            resena_stevila.add(list(mnozice[i][k])[0])
                    # ce imamo se neresena polja
                    if len(resena_stevila) != right_num:
                        new_right = right - sum(resena_stevila)
                        new_right_num = right_num - len(resena_stevila)
                        nova_mozna_st = mozna_stevila(new_right_num, new_right)
                        nova_mozna_st = nova_mozna_st.difference(resena_stevila)
                        # posodobimo mrezo
                        for k in range(j + 1, j + right_num + 1):
                            if len(mnozice[i][k]) != 1:
                                mnozice[i][k] = mnozice[i][k].intersection(nova_mozna_st)
                        # preverimo ce so kaksne kombinacije odvec in odstranimo odvecne
                        if len(mnozice[i][j][1][0]) > 1:
                            odstrani = []
                            for k in range(j + 1, j + right_num + 1):
                                for m in mnozice[i][j][1][0]:
                                    if len(set(m).intersection(mnozice[i][k])) == 0:
                                        odstrani.append(m)
                            # ce smo nasli odvecne, se jih znebimo
                            if len(odstrani) != 0:
                                for o in odstrani:
                                    # preverjamo, ker ga lahko po nesreci veckrat odstranimo
                                    if o in mnozice[i][j][1][0]:
                                        mnozice[i][j][1][0].remove(o)
                                tmp = set()
                                for m in mnozice[i][j][1][0]:
                                    tmp = tmp.union(m)
                                for k in range(j + 1, j + right_num + 1):
                                    mnozice[i][k] = mnozice[i][k].intersection(tmp)
                        #TODO sedaj pogledamo če lahko kaj generiramo
                        kombinacije = mnozice[i][j][1][0]
                        stev = []
                        nove_stev = []
                        for k in range(j + 1, j + right_num + 1):
                            stev.append(mnozice[i][k])
                            nove_stev.append(set())
                        odstrani = []
                        for ko in kombinacije:
                            perm_komb = list(permutations(ko))
                            # preverimo ce je permutacija ok
                            ok_kombinacija = False
                            for p in perm_komb:
                                # preverimo ce je iteracija permutacije ok
                                ok_iteracija = True
                                for ix, s in enumerate(stev):
                                    if len(s.intersection({p[ix]})) == 0:
                                        ok_iteracija = False
                                if ok_iteracija == True:
                                    ok_kombinacija = True
                                    for ix in range(len(nove_stev)):
                                        nove_stev[ix] = nove_stev[ix].union({p[ix]})
                            if ok_kombinacija == False:
                                odstrani.append(ko)
                        for o in odstrani:
                            if o in mnozice[i][j][1][0]:
                                mnozice[i][j][1][0].remove(o)
                        for k, nov in enumerate(nove_stev):
                            mnozice[i][j+k+1] = nov

    stResenih = 0
    for i in range(0, length):
        for j in range(0, high):
            # ce je mozna le ena stevilka jo vpisemo v igro
            if len(mnozice[i][j]) == 1:
                stResenih += 1
                game[i][j] = list(mnozice[i][j])[0]
    #TODO sedaj je potrebno nekaj narediti v zvezi s kombinacijami tm gor
    return stResenih


if __name__ == "__main__":
    set_of_number = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # 8 x 8 kakuro
    kakuro_8x8_N = [[(0, 0), (23, 0), (30, 0), (0, 0), (0, 0), (27, 0), (12, 0), (16, 0)],
                  [(0, 16), 0, 0, (0, 0), (17, 24), 0, 0, 0],
                  [(0, 17), 0, 0, (15, 29), 0, 0, 0, 0],
                  [(0, 35), 0, 0, 0, 0, 0, (12, 0), (0, 0)],
                  [(0, 0), (0, 7), 0, 0, (7, 8), 0, 0, (7, 0)],
                  [(0, 0), (11, 0), (10, 16), 0, 0, 0, 0, 0],
                  [(0, 21), 0, 0, 0, 0, (0, 5), 0, 0],
                  [(0, 6), 0, 0, 0, (0, 0), (0, 3), 0, 0]]
    kakuro_8x8_N = np.array(kakuro_8x8_N)

    kakuro_8x8_S = [[(0, 0), (23, 0), (30, 0), (0, 0), (0, 0), (27, 0), (12, 0), (16, 0)],
                  [(0, 16), 9, 7, (0, 0), (17, 24), 8, 7, 9],
                  [(0, 17), 8, 9, (15, 29), 8, 9, 5, 7],
                  [(0, 35), 6, 8, 5, 9, 7, (12, 0), (0, 0)],
                  [(0, 0), (0, 7), 6, 1, (7, 8), 2, 6, (7, 0)],
                  [(0, 0), (11, 0), (10, 16), 4, 6, 1, 3, 2],
                  [(0, 21), 8, 9, 3, 1, (0, 5), 1, 4],
                  [(0, 6), 3, 1, 2, (0, 0), (0, 3), 2, 1]]

    # 6 x 6 kakuro expert
    kakuro_6x6_N = [[(0, 0), (0, 0), (27, 0), (14, 0), (33, 0), (20, 0)],
                    [(0, 0), (0, 28), 0, 0, 0, 0],
                    [(0, 0), (12, 15), 0, 0, 0, 0],
                    [(0, 12), 0, 0, (4, 17), 0, 0],
                    [(0, 26), 0, 0, 0, 0, (0, 0)],
                    [(0, 12), 0, 0, 0, 0, (0, 0)]]
    kakuro_6x6_N = np.array(kakuro_6x6_N)

    kakuro_6x6_S = [[(0, 0), (0, 0), (27, 0), (14, 0), (33, 0), (20, 0)],
                    [(0, 0), (0, 28), 4, 8, 7, 9],
                    [(0, 0), (12, 15), 1, 6, 5, 3],
                    [(0, 12), 4, 8, (4, 17), 9, 8],
                    [(0, 26), 6, 9, 3, 8, (0, 0)],
                    [(0, 12), 2, 5, 1, 4, (0, 0)]]

    # 5 x 5 kakuro
    kakuro_5x5_N = [
        [(0, 0), (8, 0), (24, 0), (0, 0), (0, 0)],
        [(0, 15), 0, 0, (19, 0), (0, 0)],
        [(0, 10), 0, 0, 0, (9, 0)],
        [(0, 0), (0, 19), 0, 0, 0],
        [(0, 0), (0, 0), (0, 16), 0, 0],
    ]
    kakuro_5x5_N = np.array(kakuro_5x5_N)

    kakuro_5x5_S = [
        [(0,0), (8, 0), (24,0), (0,0), (0,0) ],
        [(0, 15), 7, 8, (19, 0), (0, 0)],
        [(0, 10), 1, 7, 2, (9, 0)],
        [(0, 0), (0, 19), 9, 8, 2],
        [(0, 0), (0, 0), (0, 16), 9, 7],
    ]

    # 4 x 4 kakuro
    kakuro_4x4_N = [
        [(0, 0), (23, 0), (9, 0), (7, 0)],
        [(0, 18), 0, 0, 0],
        [(0, 11), 0, 0, 0],
        [(0, 10), 0, 0, 0],
    ]
    kakuro_4x4_N = np.array(kakuro_4x4_N)

    kakuro_4x4_S = [
        [(0, 0), (23, 0), (9, 0), (7, 0)],
        [(0, 18), 9, 5, 4],
        [(0, 11), 8, 1, 2],
        [(0, 10), 6, 3, 1],
    ]

    # 3 x 3 kakuro
    kakuro_3x3_N = [
        [(0, 0), (10, 0), (8, 0)],
        [(0, 14), 0, 0],
        [(0, 4), 0, 0],
    ]
    kakuro_3x3_N = np.array(kakuro_3x3_N)

    kakuro_3x3_N_B = "2 2\n" \
           "14 A1 A2\n" \
           "4 B1 B2\n" \
           "10 A1 B1\n" \
           "8 A2 B2"

    kakuro_3x3_S = [
        [(0, 0), (10, 0), (8, 0)],
        [(0, 14), 9, 5],
        [(0, 4), 1, 3],
    ]

    #TODO vzamemo eno od iger _______________________________________HAHAHAHAHAHA___________________________________
    game = kakuro_6x6_N

    length_game = len(game)
    high_game = len(game[0])

    print(DataFrame(game).to_string(header=False))

    mn, stPolj, stResenih = algoritem_init(game, length_game, high_game)
    # postopek se zaključi, ko resimo vsa polja
    iter = 0
    print("Iteracija:", iter, "Število rešenih: ", stResenih)
    while stResenih < stPolj:
        iter += 1
        stResenih = algoritem_solve(game, length_game, high_game, mn)
        print("Iteracija:", iter, "Število rešenih: ", stResenih)


    #TODO olepšaj kodo -> ustrezni komentarji
    #TODO ustrezen izpis (po vrsticah), dodano merjenje časa cez vse kakurote
    #TODO dopolni predlogo

    print(DataFrame(game).to_string(header=False))


    STEPS = 10
    sum_time = 0
    for i in range (0, STEPS):
        # init cas
        start_time = time.time()
        # pozenes algoritem
        backtracing.start_backtracing(kakuro_3x3_N_B, kakuro_3x3_N, False)
        seconds = (time.time() - start_time)
        # pristejemo cas trenutne iteracije skupnem casu
        sum_time += seconds
        #print("--- %s seconds ---" % seconds)

    average_time = sum_time / STEPS
    #print(average_time)

