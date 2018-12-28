import numpy as np
import collections


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


# np_array = np.array([2, 2, 3, 4, 5, 6, 7, 8, 9])
set_of_number = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

# a = check_duplicate_number(np_array, set_of_number)


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

# change only np_kakuro_1_N array
# print(np_kakuro_1_N)
# np_kakuro_1_N[0][0] = 1
# print(kakuro_1_N)
# print(np_kakuro_1_N)


# print(np_kakuro_1_N[0])  # first row
# print(np_kakuro_1_N[:, 0])  # first column


game = np_kakuro_1_N

length_game = len(game)

high_game = len(game[0])

down_num = 0
right_num = 0

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

print(game)
