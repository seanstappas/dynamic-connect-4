from __future__ import print_function

NUM_ROWS = 7
NUM_COLS = 7
DIRECTIONS = ('E', 'W', 'N', 'S')
MOVEMENT_DIFFS = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0)
}
X_MOVEMENT_DIFFS = {
    'N': 0,
    'S': 0,
    'E': 1,
    'W': -1
}
Y_MOVEMENT_DIFFS = {
    'N': -1,
    'S': 1,
    'E': 0,
    'W': 0
}


def actions_and_successors(state, white_player=True):
    """
    Returns a list of action, successor tuples resulting from the given state.

    :param state: the state to get successors of
    :param white_player: True if the current player is white, False otherwise
    :return: a list of action, successor tuples resulting from the given state.
    """
    return [(a, result(state, a, white_player)) for a in actions(state, white_player)]


def print_state(state):
    """
    Prints the given state.

    :param state: the state to print
    """
    print(' ', end=' ')
    for col in range(NUM_COLS):
        print(col + 1, end=' ')
    print()

    for row in range(NUM_ROWS):
        print(row + 1, end=' ')
        for col in range(NUM_COLS):
            if (col + 1, row + 1) in state[0]:
                print('O', end='')
            elif (col + 1, row + 1) in state[1]:
                print('X', end='')
            else:
                print(' ', end='')
            if col < NUM_COLS - 1:
                print(',', end='')
        print()


def str_to_state(str_state):
    """
    Returns a state corresponding to the provided string representation. Here is an example of a valid state:
     , , , , , ,X
     , , , , ,X,
     , , , , ,O,X
     ,X,O, , , ,X
     , , , , ,O,
     ,O,X, , , ,
    O, , , ,O, ,

    :param str_state: a string representation of the board
    :return: the corresponding state
    """
    white_squares = []
    black_squares = []
    y = 1
    for row in str_state.splitlines():
        x = 1
        for square in row.split(','):
            if square == ',':
                continue
            if square == 'O':
                white_squares.append((x, y))
            elif square == 'X':
                black_squares.append((x, y))
            x += 1
        y += 1
    return tuple(white_squares), tuple(black_squares)


def is_within_bounds(x, y):
    """
    :return: True if the given x, y coordinates are within the bounds of the board
    """
    return 0 < x <= NUM_COLS and 0 < y <= NUM_ROWS


def is_free_square(state, x, y):
    """
    :return: True if the given x, y coordinates are free spots, given the provided state
    """
    return (x, y) not in state[0] and (x, y) not in state[1]


def is_valid_action(state, x, y, direction):
    """
    Checks if moving the piece at given x, y coordinates in the given direction is valid, given the current state.

    :param state: the current state
    :param x: the x coordinate of the piece
    :param y: the y coordinate of the piece
    :param direction: the direction to travel with this action
    :return: True if the action is valid, False otherwise
    """
    new_x = x + X_MOVEMENT_DIFFS[direction]
    new_y = y + Y_MOVEMENT_DIFFS[direction]
    return is_within_bounds(new_x, new_y) and is_free_square(state, new_x, new_y)


def occupied_squares_by_player(state, white_player):
    """
    Returns the the x, y coordinates of the squares occupied by the given player.

    :param state: the given state
    :param white_player: True if the current player is white, False otherwise
    :return: the x, y coordinates of the squares occupied by the given player.
    """
    return state[0] if white_player else state[1]


def actions(state, white_player=True):
    """
    Returns the actions available to the given player in the given state.

    :param state: the current state
    :param white_player: True if the current player is white, False otherwise
    :return: the actions available to the given player in the given state
    """
    return [(x, y, direction)
            for (x, y) in occupied_squares_by_player(state, white_player)
            for direction in DIRECTIONS
            if is_valid_action(state, x, y, direction)]


def action_str_to_tuple(a):
    """
    Converts the provided action string to a tuple

    :param a: the action, in string form. For example: '13E'.
    :return: the action in tuple form
    """
    if a is not None and '1' <= a[0] <= '7' and '1' <= a[1] <= '7' and a[2] in DIRECTIONS:
        return int(a[0]), int(a[1]), a[2]
    else:
        return None


def action_tuple_to_str(action):
    """
    Converts the provided action tuple to a string.

    :param action: the action
    :return: a string representation of the action tuple
    """
    if action is None:
        return None
    return str(action[0]) + str(action[1]) + action[2]


def result(state, action, white_player=True):
    """
    Returns the resulting state when the given action is applied to the given state.

    :param state: the current state
    :param action: the action to apply
    :param white_player: True if the current player is white, False otherwise
    :return: the resulting state when the given action is applied to the given state
    """
    if white_player:
        return result_tuple(state, action, white_player), state[1]
    else:
        return state[0], result_tuple(state, action, white_player)


def result_tuple(s, a, white_player):
    """
    Returns the x, y coordinates of the pieces of the given player when the given action is applied to the given state.

    :param s: the current state
    :param a: the action to apply
    :param white_player: True if the current player is white, False otherwise
    :return: the x, y coordinates of the pieces of the given player when the given action is applied to the given state
    """
    old_x = a[0]
    old_y = a[1]
    direction = a[2]
    new_x = old_x + X_MOVEMENT_DIFFS[direction]
    new_y = old_y + Y_MOVEMENT_DIFFS[direction]
    return tuple((x, y) if x != old_x or y != old_y else (new_x, new_y)
                 for (x, y) in occupied_squares_by_player(s, white_player))


def file_to_state(file_name):
    """
    Converts the board given by the provided file to a state. Here is an example of a valid state:
     , , , , , ,X
     , , , , ,X,
     , , , , ,O,X
     ,X,O, , , ,X
     , , , , ,O,
     ,O,X, , , ,
    O, , , ,O, ,

    :param file_name: the name of the file containing the state
    :return: a state corresponding to the board
    """
    with open(file_name, 'r') as state_file:
        string_state = state_file.read()
        state = str_to_state(string_state)
        return state
