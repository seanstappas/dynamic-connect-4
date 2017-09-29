from connect_four import file_to_state, actions, action_tuple_to_str, print_state


def print_actions(state):
    print_state(state)
    print('Possible actions: for white {}'.format([action_tuple_to_str(a) for a in actions(state, True)]))
    print('Possible actions: for black {}'.format([action_tuple_to_str(a) for a in actions(state, False)]))


if __name__ == '__main__':
    for i in range(9):
        s = file_to_state('states/test_state_{}.txt'.format(i))
        print_actions(s)
        if i == 1:
            for j in range(7):
                s = file_to_state('states/test_state_{}_blocked_{}.txt'.format(i, j))
                print_actions(s)