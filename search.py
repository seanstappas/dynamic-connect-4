import random
import time

from connect_four import actions_and_successors, action_tuple_to_str
from heuristics import default_heuristic, is_winning_heuristic, WIN_HEURISTIC, win_loss_heuristic

INF = float("inf")

NO_ORDER = 0
SORTED_BY_HEURISTIC_ORDER = 1
RANDOM_ORDER = 2

EXACT = 0
LOWER_BOUND = -1
UPPER_BOUND = 1


def minimax(state, depth, transposition_table, white_player, count=False):
    """
    Implementation of the minimax search algorithm, inspired from https://en.wikipedia.org/wiki/Minimax.

    :param state: the current state
    :param depth: the search cut-off depth
    :param transposition_table: the transposition table
    :param white_player: True if the current player is white, False otherwise
    :param count: True to keep count of the number of times it is called (i.e. the number of states explored), False
    otherwise. If this is set, the "counter" method reference should be set to zero before calling this method.
    :return: the best value for the current player
    """
    if count:
        minimax.counter += 1
    if (state, depth) in transposition_table:
        return transposition_table[(state, depth)]
    win_h = win_loss_heuristic(state)
    if depth == 0 or is_winning_heuristic(win_h):
        return win_h

    if white_player:
        best_value = -INF
        for action, successor in actions_and_successors(state, white_player):
            v = minimax(successor, depth - 1, transposition_table, not white_player, count)
            best_value = max(best_value, v)
        transposition_table[(state, depth)] = best_value
        return best_value

    else:
        best_value = INF
        for action, successor in actions_and_successors(state, white_player):
            v = minimax(successor, depth - 1, transposition_table, not white_player, count)
            best_value = min(best_value, v)
        transposition_table[(state, depth)] = best_value
        return best_value


def alphabeta(state, depth, transposition_table, time_limit, start_time, alpha, beta, white_player, count=False):
    """
    Implementation of the alpha-beta search algorithm, inspired from https://en.wikipedia.org/wiki/Alpha-beta_pruning.
    Note that the final implementation of alpha-beta used is with the negamax algorithm (see negamax method).

    :param state: the current state
    :param depth: the cut-off depth
    :param transposition_table: the transposition table
    :param time_limit: the time limit for the search
    :param start_time: the time at which the search was started
    :param alpha: alpha value
    :param beta: beta value
    :param white_player: True if the current player is white, False otherwise
    :param count: True to keep count of the number of times it is called (i.e. the number of states explored), False
    otherwise. If this is set, the "counter" method reference should be set to zero before calling this method.
    :return: an (action, value) tuple, where action is the best action available to the current player and value is the
    best value
    """
    if count:
        alphabeta.counter += 1
    elapsed_time = time.time() - start_time
    win_h = win_loss_heuristic(state)
    if is_winning_heuristic(win_h):
        return None, win_h * depth  # Shallower wins are better
    if depth == 0 or elapsed_time >= time_limit:
        return None, default_heuristic(state)
    if (state, depth) in transposition_table:
        return None, transposition_table[(state, depth)]
    succs = actions_and_successors(state, white_player)
    succs.sort(key=lambda succ: default_heuristic(succ[1]), reverse=white_player)
    best_action = None
    if white_player:
        v = -INF
        for action, successor in succs:
            _, succ_value = alphabeta(successor, depth - 1, transposition_table, time_limit, start_time, alpha, beta,
                                      not white_player, count)
            if succ_value > v:
                v = succ_value
                best_action = action
            alpha = max(alpha, v)
            if beta <= alpha:
                break  # (* beta cut-off *)
        transposition_table[(state, depth)] = v
        return best_action, v
    else:
        v = INF
        for action, successor in succs:
            _, succ_value = alphabeta(successor, depth - 1, transposition_table, time_limit, start_time, alpha, beta,
                                      not white_player, count)
            if succ_value < v:
                v = succ_value
                best_action = action
            beta = min(beta, v)
            if beta <= alpha:
                break  # (* alpha cut-off *)
        transposition_table[(state, depth)] = v
        return best_action, v


def negamax(state, depth, alpha, beta, transposition_table, time_limit, start_time, color, count=False,
            order=SORTED_BY_HEURISTIC_ORDER, heuristic=default_heuristic):
    """
    Implementation of the negamax search algorithm, which is a flavour of alpha-beta search. Inspired from
    https://en.wikipedia.org/wiki/Negamax. This is the final alpha-beta algorithm used by the program.

    :param state: the current state
    :param depth: the depth cut-off
    :param alpha: the alpha value
    :param beta: the beta value
    :param transposition_table: the transposition table
    :param time_limit: the time limit for the search
    :param start_time: the time at which the search was started
    :param color: 1 if the current player is white, -1 otherwise
    :param count: True to keep count of the number of times it is called (i.e. the number of states explored), False
    otherwise. If this is set, the "counter" method reference should be set to zero before calling this method.
    :param order: the order in which successors should be sorted before being explored. If set to SORTED_ORDER,
    successors will be sorted by the best heuristic value for the current player. If set to RANDOM_ORDER, the
    successors will be arranged randomly. Otherwise, no ordering is imposed.
    :param heuristic: the heuristic to apply
    :return: an (action, value) tuple, where action is the best action available to the current player and value is the
    best value
    """
    if count:
        negamax.counter += 1

    # Win condition
    win_h = win_loss_heuristic(state)
    if is_winning_heuristic(win_h):
        return None, color * win_h

    if depth == 0:
        return None, color * heuristic(state)

    # Time limit check
    if time.time() - start_time >= time_limit:
        return None, None

    alpha_orig = alpha

    # Check transposition table
    if state in transposition_table:
        tt_entry = transposition_table[state]
        if tt_entry[2] >= depth:
            val = tt_entry[0]
            flag = tt_entry[1]
            if flag == EXACT:
                return None, val
            elif flag == LOWER_BOUND:
                alpha = max(alpha, val)
            elif flag == UPPER_BOUND:
                beta = min(beta, val)
            if alpha >= beta:
                return None, val

    # Ordering
    white_player = color == 1
    actions_successors = actions_and_successors(state, white_player)
    if order == SORTED_BY_HEURISTIC_ORDER:
        actions_successors.sort(key=lambda act_succ: heuristic(act_succ[1]), reverse=white_player)
    elif order == RANDOM_ORDER:
        random.shuffle(actions_successors)

    # Visit children
    best_value = -INF
    best_action = None
    for action, child in actions_successors:
        _, v = negamax(child, depth - 1, -beta, -alpha, transposition_table, time_limit, start_time, -color, count,
                       order, heuristic)
        if v is None:
            # Time limit reached at lower level
            return None, None
        v = -v
        if v > best_value:
            best_value = v
            best_action = action
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    # Save to transposition table
    flag = EXACT
    if best_value <= alpha_orig:
        flag = UPPER_BOUND
    elif best_value >= beta:
        flag = LOWER_BOUND
    transposition_table[state] = (best_value, flag, depth)

    return best_action, best_value


def iterative_dfs_negamax(state, time_limit, depth_limit, white_player, heuristic=default_heuristic):
    """
    Applies iterative deepening search with the negamax search algorithm.

    :param state: the current state
    :param time_limit: the time limit for the search
    :param depth_limit: the maximum depth to search to
    :param white_player: True if the current player is white, False otherwise
    :param heuristic: the heuristic to apply
    :return: the best action for the current player
    """
    start_time = time.time()
    transposition_table = {}
    last_best_action = None
    last_time = 0
    player = 'White' if white_player else 'Black'
    print('[{} AI] Thinking of a move...'.format(player))
    for d in range(depth_limit):
        t = time.time()
        negamax.counter = 0
        best_action, v = negamax(state, d, -INF, INF, transposition_table, time_limit, start_time,
                                 1 if white_player else -1, count=True,
                                 heuristic=heuristic)
        if v is None:  # Incomplete search
            return last_best_action
        root_value = v if white_player else -v
        elapsed_time = time.time() - t
        print('[{} AI] Depth {}, value: {}, best action: {}, elapsed time: {} s, states visited: {}'
              .format(player, d, root_value, action_tuple_to_str(best_action), str(elapsed_time)[:4], negamax.counter))

        if elapsed_time > last_time:
            last_best_action = best_action
        last_time = elapsed_time
        if white_player and root_value >= WIN_HEURISTIC or not white_player and root_value <= -WIN_HEURISTIC:
            print('[AI] Win found for {} player with move {}'.format(
                player,
                action_tuple_to_str(best_action)))
            return best_action
        if time.time() - start_time >= time_limit:
            return last_best_action
    return last_best_action
