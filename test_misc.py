import time

from connect_four import print_state, actions, result, action_str_to_tuple, actions_and_successors, str_to_state
from heuristics import default_heuristic
from search import alphabeta, INF

if __name__ == '__main__':
    initial_state = (
        (
            (1, 3), (1, 5), (1, 7), (7, 2), (7, 4), (7, 6)  # White player O (plays first)
        ),
        (
            (1, 2), (1, 4), (1, 6), (7, 1), (7, 3), (7, 5)  # Black player X
        ),
    )

    print_state(initial_state)
    print('Heuristic:', default_heuristic(initial_state))

    print('White actions:', actions(initial_state))
    print('Black actions:', actions(initial_state, white_player=False))

    print('Action 13E:')
    print_state(result(initial_state, action_str_to_tuple('13E')))

    print('All actions:')
    for _, c in actions_and_successors(initial_state):
        print_state(c)
        print('Heuristic:', default_heuristic(c))

    string_state = ' , , , , , , \n\
     , , , , , , \n\
    O, ,X, , , , \n\
     , , ,O, , ,X\n\
     , , , ,O,X,X\n\
     , ,O, , ,O,X\n\
     , , ,X,O, , \n\
    '

    print(string_state)
    state = str_to_state(string_state)
    print_state(state)
    # print('H: ', heuristic(state))

    string_state = ' , , , , , , \n\
     , , , , , , \n\
    O, ,O, , , , \n\
     , , ,X, , ,X\n\
     , , , ,O,X,X\n\
     , ,O, , ,X,X\n\
     , , ,X,X, , \n\
    '

    print(string_state)
    state = str_to_state(string_state)
    print_state(state)
    print('H: ', default_heuristic(state))

    string_state = ' , , , , , , \n\
, , , , , , \n\
, , , , , , \n\
, , , , , , \n\
, , , , , , \n\
O,O,O, , , , \n\
, , , ,O, , \n\
    '
    print(string_state)
    state = str_to_state(string_state)
    print(state)
    print_state(state)
    print('Hzzz: ', default_heuristic(state))

    string_state = 'X, , , , , ,X\n\
 , , , ,O, , \n\
O, , , , ,X, \n\
 , , , ,X, ,O\n\
 ,O, , ,X,O,O\n\
 , , , ,X, , \n\
 , , , , , , \n'
    print(string_state)
    state = str_to_state(string_state)
    print(state)
    print_state(state)
    print('Hzzz: ', default_heuristic(state))

    succs = actions_and_successors(state)

    time_limit = 5
    start_time = time.time()
    transposition_table = {}
    for d in range(5):
        new_table = {}
        alphabeta(state, new_table,  new_table, d, time_limit, start_time, -INF, INF)
        if time.time() - start_time >= time_limit:
            break
        if len(new_table) > len(transposition_table):
            transposition_table = new_table

    def cache(succ):
        return transposition_table[succ]


    old_table = transposition_table
    succs = actions_and_successors(state)
    print('Unsorted succs: {}'.format(succs))
    print('Sorted succs: {}'.format(succs))

    with open('states/state1.txt', 'r') as file1:
        string_state = file1.read()
    print(string_state)
    state = str_to_state(string_state)
    print(state)
    print_state(state)
    print('Hzzz: ', default_heuristic(state))

    with open('states/state2.txt', 'r') as file2:
        string_state = file2.read()
    print(string_state)
    state = str_to_state(string_state)
    print(state)
    print_state(state)
    print('Hzzz: ', default_heuristic(state))

