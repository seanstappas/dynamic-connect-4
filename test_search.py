from connect_four import file_to_state, print_state
from search import iterative_dfs_negamax

if __name__ == '__main__':
    state = file_to_state('states/test_state_search_1.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 5, white_player=False)

    state = file_to_state('states/test_state_search_2.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 5, white_player=True)

    state = file_to_state('states/test_state_search_3.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 5, white_player=False)

    state = file_to_state('states/test_state_search_4.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 5, white_player=False)

    state = file_to_state('states/test_state_search_5.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 10, white_player=True)

    state = file_to_state('states/test_state_search_6.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 10, white_player=True)

    state = file_to_state('states/test_state_Sep23.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 10, white_player=True)

    state = file_to_state('states/test_state_Sep23_1.txt')
    print_state(state)
    action = iterative_dfs_negamax(state, 20, 10, white_player=False)

