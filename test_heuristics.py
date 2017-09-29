from heuristics import default_heuristic, is_winning_state
from connect_four import file_to_state, print_state


def print_heuristic(state):
    print_state(state)
    h = default_heuristic(state)
    print('Heurisitic: {}, win: {}'.format(h, is_winning_state(state)))


if __name__ == '__main__':
    print('Final bug:')
    print_heuristic(file_to_state('states/state_bug.txt'))
    for i in range(10):
        print('Test State {}'.format(i))
        s = file_to_state('states/test_state_{}.txt'.format(i))
        print_heuristic(s)
        if i == 1:
            for j in range(7):
                s = file_to_state('states/test_state_{}_blocked_{}.txt'.format(i, j))
                print_heuristic(s)
    for i in range(4):
        s = file_to_state('states/test_state_win_{}.txt'.format(i))
        print_heuristic(s)
    for i in range(4):
        s = file_to_state('states/test_state_close_to_win_{}.txt'.format(i))
        print_heuristic(s)
