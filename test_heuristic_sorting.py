from connect_four import file_to_state, print_state, actions_and_successors
from heuristics import default_heuristic


def print_sorted_succesors(state, white_player=True, depth=1):
    for i in range(depth):
        print('Initial state (depth {}):'.format(i))
        print_state(state)
        actions_succ = actions_and_successors(state, white_player)
        actions_succ.sort(key=lambda act_succ: default_heuristic(act_succ[1]), reverse=white_player)
        print('Sorted by heuristic:')
        for a, succ in actions_succ:
            print_state(succ)
            print('Heuristic: {}'.format(default_heuristic(succ)))
        state = actions_succ[0][1]
        white_player = not white_player


if __name__ == '__main__':
    s = file_to_state('states/test_state_Sep23.txt')
    print_sorted_succesors(s, white_player=True, depth=2)
