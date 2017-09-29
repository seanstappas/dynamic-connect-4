import random

from connect_four import NUM_COLS, NUM_ROWS, actions

WIN_HEURISTIC = 10000
FOUR_IN_A_ROW_HEURISTIC = 3000
THREE_IN_A_ROW_HEURISTIC = 1000
ADJACENT_DIRECTIONS = ((0, 1), (1, -1), (1, 0), (1, 1))  # Only need to consider half, since all x,y tuples explored

CENTER_X = (NUM_COLS + 1) / 2
CENTER_Y = (NUM_ROWS + 1) / 2


def default_heuristic(state):
    """
    The heuristic used by default by the search algorithms.
    
    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    return weighted_distance_to_center_heuristic(state) + count_num_in_a_row_heuristic(state)


def count_num_in_a_row_heuristic(state):
    """
    Heuristic which returns a value associated with the number of pieces arranged in a line, where 3 in a line is better
    than 2 in a line. Note: only counts 3 in a row once.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    def count_pieces_in_a_row(pieces, enemy_pieces):
        total_count = 0
        for (x, y) in pieces:
            for (i, j) in ADJACENT_DIRECTIONS:
                new_x = x + i
                new_y = y + j
                count = 1
                while (new_x, new_y) in pieces:
                    count += 1
                    new_x += i
                    new_y += j
                if (new_x, new_y) not in enemy_pieces:  # Blank connector
                    new_x += i
                    new_y += j
                while (new_x, new_y) in pieces:
                    count += 1
                    new_x += i
                    new_y += j
                if count >= 4:
                    return FOUR_IN_A_ROW_HEURISTIC
                if count >= 3:
                    return THREE_IN_A_ROW_HEURISTIC
                total_count += count * count  # Bigger counts better...
        return total_count

    white_squares = state[0]
    black_squares = state[1]
    return count_pieces_in_a_row(white_squares, black_squares) - count_pieces_in_a_row(black_squares, white_squares)


def weighted_distance_to_center_heuristic(state):
    """
    Heuristic which computes a sum of weighted distances between the pieces and the center of the board, where the
    distance x, y coordinates are given by the squares of their respective Manhattan counterparts.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    def distance_to_center(pieces):
        distance = 0
        for (x, y) in pieces:
            diff_x = x - CENTER_X
            diff_y = y - CENTER_Y
            distance += diff_x * diff_x + diff_y * diff_y
        return distance

    white_pieces = state[0]
    black_pieces = state[1]

    return distance_to_center(black_pieces) - distance_to_center(white_pieces)


def random_heuristic(state):
    """
    Heuristic which returns a random number, independent of the given state.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    return random.randint(-WIN_HEURISTIC + 1, WIN_HEURISTIC - 1)


def has_three_in_a_row_heuristic(state):
    """
    Heuristic which simply checks whether a player has three pieces in a line.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_squares = state[0]
    black_squares = state[1]

    def has_three_pieces_in_a_row(pieces, enemy_pieces):
        for (x, y) in pieces:
            for (i, j) in ADJACENT_DIRECTIONS:
                new_x = x + i
                new_y = y + j
                count = 1
                while (new_x, new_y) in pieces:
                    count += 1
                    new_x += i
                    new_y += j
                if (new_x, new_y) not in enemy_pieces:  # Blank connector
                    new_x += i
                    new_y += j
                while (new_x, new_y) in pieces:
                    count += 1
                    new_x += i
                    new_y += j
                if count >= 3:  # Bigger counts better...
                    return 1
        return 0

    white_three_in_a_row = has_three_pieces_in_a_row(white_squares, black_squares)
    black_three_in_a_row = has_three_pieces_in_a_row(black_squares, white_squares)
    return white_three_in_a_row - black_three_in_a_row


def close_to_the_edge_heuristic(state):
    """
    Heuristic which computes how close to the edge the pieces are.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_squares = state[0]
    black_squares = state[1]

    def cnt(x):
        return x if x < 4 else 7 - x + 1

    def count_squares_on_edge(squares):
        count = 0
        for (x, y) in squares:
            count += cnt(x)
            count += cnt(y)
        return count

    white_count = count_squares_on_edge(white_squares)
    black_count = count_squares_on_edge(black_squares)

    return white_count - black_count


def win_loss_heuristic(state):
    """
    Heuristic which simply computes if the given state is a win or loss for any player.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_squares = state[0]
    black_squares = state[1]

    def is_win(squares):
        for x, y in squares:
            for i, j in ADJACENT_DIRECTIONS:
                new_x = x + i
                new_y = y + j
                count = 1
                while (new_x, new_y) in squares:
                    count += 1
                    new_x += i
                    new_y += j
                if count >= 4:
                    return True
        return False

    if is_win(black_squares):
        return -WIN_HEURISTIC
    elif is_win(white_squares):
        return WIN_HEURISTIC
    else:
        return 0


def manhattan_distance_to_center_heuristic(state):
    """
    Heuristic which computes the sum of Manhattan distances between pieces and the center of the board, i.e.
    abs(x - CENTER_X) + abs(y - CENTER_Y).

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_pieces = state[0]
    black_pieces = state[1]

    def distance_to_center(pieces):
        distance = 0
        for (x, y) in pieces:
            distance += abs(x - CENTER_X) + abs(y - CENTER_Y)
        return distance

    return distance_to_center(black_pieces) - distance_to_center(white_pieces)


def distance_between_pieces_heuristic(state):
    """
    Heuristic which computes a sum of the distances between pieces of the same colour.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_pieces = state[0]
    black_pieces = state[1]

    def distance_pieces(pieces):
        distance = 0
        for (x, y) in pieces:
            min_dist = 7
            for (x2, y2) in pieces:
                if x != x2 and y != y2:
                    min_dist = min(min_dist, abs(x - x2) + abs(y - y2))
            distance += min_dist
        return distance

    return distance_pieces(black_pieces) - distance_pieces(white_pieces)


def num_actions_heuristic(state):
    """
    Heuristic which computes how many actions are available to each player.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_actions = len(actions(state, white_player=True))
    black_actions = len(actions(state, white_player=False))

    return white_actions - black_actions


def distance_from_center_and_other_pieces_heuristic(state):
    """
    Heuristic which computes a sum combining the weighted distance between pieces and the center of the board, as well
    as the distance between pieces of the same colour.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_pieces = state[0]
    black_pieces = state[1]

    center_x = (NUM_COLS + 1) / 2
    center_y = (NUM_ROWS + 1) / 2

    total_distance = 0

    for (x, y) in white_pieces:
        for (x2, y2) in white_pieces:
            total_distance -= abs(x - x2) + abs(y - y2)
        total_distance -= abs(x - center_x) + abs(y - center_y)

    for (x, y) in black_pieces:
        for (x2, y2) in black_pieces:
            total_distance += abs(x - x2) + abs(y - y2)
        total_distance += abs(x - center_x) + abs(y - center_y)

    return total_distance


def cluster_heuristic(state):
    """
    Heuristic which computes how many pieces of the same colour are adjacent to others of the same colour.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_squares = state[0]
    black_squares = state[1]

    def num_clustered(squares):
        count = 0
        for x, y in squares:
            for i, j in ADJACENT_DIRECTIONS:
                if (x + i, y + j) in squares:
                    count += 1
        return count

    return num_clustered(white_squares) - num_clustered(black_squares)


def distance_between_pieces(state):
    """
    Heuristic which computes how many pieces of the same colour are adjacent to others of the same colour.

    :param state: the state to compute the heuristic of
    :return: the heuristic value of the given state, where bigger values are better for the maximizing player
    """
    white_squares = state[0]
    black_squares = state[1]

    def dist_between(squares):
        count = 0
        for x, y in squares:
            for i, j in ADJACENT_DIRECTIONS:
                if (x + i, y + j) in squares:
                    count += 1
        return count

    return dist_between(white_squares) - dist_between(black_squares)


def is_winning_heuristic(heuristic_value):
    """
    Returns True if the given heuristic value corresponds to a win, False otherwise.

    :param heuristic_value: the heuristic value to consider
    :return: True if the given heuristic value corresponds to a win, False otherwise.
    """
    return abs(heuristic_value) >= WIN_HEURISTIC


def is_winning_state(state):
    """
    Returns True if the given state corresponds to a win, False otherwise.

    :param state: the state to consider
    :return: True if the given state corresponds to a win, False otherwise.
    """
    return is_winning_heuristic(win_loss_heuristic(state))