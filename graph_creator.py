import time

import pygal as pygal
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from heuristics import default_heuristic, random_heuristic, win_loss_heuristic, WIN_HEURISTIC
from search import minimax, alphabeta, INF, negamax, SORTED_BY_HEURISTIC_ORDER, NO_ORDER, RANDOM_ORDER
from connect_four import *

MIN_DEPTH = 3
MAX_DEPTH = 6

MIN_TIME = 1
MAX_TIME = 20
DEFAULT_TIME = 10000

DEFAULT_DEPTH = 20


def get_searched_states_starting_at(state, label):
    minimax_points = []
    negamax_points = []
    print('Initial state {}'.format(label))
    print_state(state)
    for d in range(MIN_DEPTH, MAX_DEPTH + 1):
        start_time = time.time()
        num_nodes, val = get_minimax_number_states_explored(state, d)
        minimax_points.append(num_nodes)
        print('Minimax explored {} nodes to return {} for a depth cutoff of {} in {} seconds.'.format(
            num_nodes,
            val,
            d,
            time.time() - start_time))

        start_time = time.time()
        num_nodes, val = get_negamax_number_states_explored(state, d)
        negamax_points.append(num_nodes)
        print('Negamax explored {} nodes to return {} for a depth cutoff of {} in {} seconds.'.format(
            num_nodes,
            val,
            d,
            time.time() - start_time))
    return minimax_points, negamax_points


def get_searched_states_with_ordering(state, label):
    no_sorting_points = []
    sorting_points = []
    random_points = []
    print('Initial state {}'.format(label))
    print_state(state)
    for d in range(MIN_DEPTH, MAX_DEPTH + 1):
        start_time = time.time()
        num_nodes, val = get_negamax_number_states_explored(state, d, order=NO_ORDER)
        no_sorting_points.append(num_nodes)
        print('Negamax explored {} nodes to return {} for a depth cutoff of {} in {} seconds with ordering {}.'.format(
            num_nodes,
            val,
            d,
            time.time() - start_time,
            'NO_ORDER'))

        start_time = time.time()
        num_nodes, val = get_negamax_number_states_explored(state, d, order=SORTED_BY_HEURISTIC_ORDER)
        sorting_points.append(num_nodes)
        print('Negamax explored {} nodes to return {} for a depth cutoff of {} in {} seconds with ordering {}.'.format(
            num_nodes,
            val,
            d,
            time.time() - start_time,
            'SORTED_ORDER'))

        start_time = time.time()
        num_nodes, val = get_negamax_number_states_explored(state, d, order=RANDOM_ORDER)
        random_points.append(num_nodes)
        print('Negamax explored {} nodes to return {} for a depth cutoff of {} in {} seconds with ordering {}.'.format(
            num_nodes,
            val,
            d,
            time.time() - start_time,
            'RANDOM_ORDER'))
    return no_sorting_points, sorting_points, random_points


def get_searched_states_with_heuristics(state, label):
    default_heur_points = []
    random_heur_points = []
    win_heur_points = []
    print('Initial state {}'.format(label))
    print_state(state)
    for t in range(MIN_TIME, MAX_TIME + 1):
        start_time = time.time()
        num_nodes = get_iterative_dfs_negamax_number_states_explored(state, t=t, heuristic=default_heuristic)
        default_heur_points.append(num_nodes)
        print('Negamax explored {} nodes in {} seconds with {} heuristic.'.format(
            num_nodes,
            time.time() - start_time,
            'DEFAULT'))

        start_time = time.time()
        num_nodes = get_iterative_dfs_negamax_number_states_explored(state, t=t, heuristic=random_heuristic)
        random_heur_points.append(num_nodes)
        print('Negamax explored {} nodes in {} seconds with {} heuristic.'.format(
            num_nodes,
            time.time() - start_time,
            'RANDOM'))

        start_time = time.time()
        num_nodes = get_iterative_dfs_negamax_number_states_explored(state, t=t, heuristic=win_loss_heuristic)
        win_heur_points.append(num_nodes)
        print('Negamax explored {} nodes in {} seconds with {} heuristic.'.format(
            num_nodes,
            time.time() - start_time,
            'WIN_LOSS'))
    return default_heur_points, random_heur_points, win_heur_points


def get_searched_states_with_heuristics_and_return_depth(state, label):
    default_heur_points = []
    random_heur_points = []
    win_heur_points = []
    print('Initial state {}'.format(label))
    print_state(state)
    start_time = time.time()
    for t in range(MIN_TIME, MAX_TIME + 1):
        depth = get_iterative_dfs_negamax_depth(state, t=t, heuristic=default_heuristic)
        default_heur_points.append(depth)
        print('Negamax explored {} nodes in {} seconds with {} heuristic.'.format(
            depth,
            time.time() - start_time,
            'DEFAULT'))

        start_time = time.time()
        depth = get_iterative_dfs_negamax_depth(state, t=t, heuristic=random_heuristic)
        random_heur_points.append(depth)
        print('Negamax explored {} nodes in {} seconds with {} heuristic.'.format(
            depth,
            time.time() - start_time,
            'RANDOM'))

        start_time = time.time()
        depth = get_iterative_dfs_negamax_depth(state, t=t, heuristic=win_loss_heuristic)
        win_heur_points.append(depth)
        print('Negamax explored {} nodes in {} seconds with {} heuristic.'.format(
            depth,
            time.time() - start_time,
            'WIN_LOSS'))
    return default_heur_points, random_heur_points, win_heur_points


def plot_with_plotly(minimax_points, alphabeta_points, negamax_points, label):
    line_chart = pygal.Line()
    line_chart.title = 'Question 1{}'.format(label)
    line_chart.x_labels = map(str, range(3, 7))
    line_chart.add('Minimax',
                   minimax_points)
    line_chart.add('Alphabeta', alphabeta_points)
    line_chart.add('Negamax', negamax_points)
    line_chart.render_to_file('question1{}.svg'.format(label))


def plot_with_pyplot_q1(minimax_points, negamax_points, label):
    d = 3
    print('Minimax q1{}'.format(label))
    for y in minimax_points:
        print('{},{}'.format(d, y))
        d += 1
    d = 3
    print('Alphabeta q1{}'.format(label))
    for y in negamax_points:
        print('{},{}'.format(d, y))
        d += 1

    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    x_range = range(MIN_DEPTH, MAX_DEPTH + 1)
    plt.plot(x_range, minimax_points, "o-", label='Minimax')
    # plt.plot(x_range, alphabeta_points, "ro-", label='Alpha-beta')
    plt.plot(x_range, negamax_points, "ro-", label='Alpha-beta')
    # plt.title('Question 1{}'.format(label))
    plt.xlabel('Depth cutoff')
    plt.ylabel('Number of states explored')
    plt.grid(True)
    plt.legend()
    # plt.show()

    for x, y in zip(x_range, minimax_points):
        if x == 3:
            plt.annotate('{}'.format(y), xy=(x, y), xytext=(0, 3), ha='right', textcoords='offset points', size=10,
                         color='#1f77b4')
        elif x == 6:
            plt.annotate('{}'.format(y), xy=(x, y), xytext=(-5, 0), ha='right', textcoords='offset points', size=10,
                         color='#1f77b4')
        else:
            plt.annotate('{}'.format(y), xy=(x, y), xytext=(-5, 5), ha='right', textcoords='offset points', size=10,
                         color='#1f77b4')
    # for x, y in zip(x_range, alphabeta_points):
    #     plt.annotate('{}'.format(y), xy=(x, y), xytext=(-10, -10), ha='right',
    #                  textcoords='offset points', size=10, color='r')
    for x, y in zip(x_range, negamax_points):
        plt.annotate('{}'.format(y), xy=(x, y), xytext=(30, -10), ha='right',
                     textcoords='offset points', size=10, color='r')

    f.savefig('plots/question1{}.pdf'.format(label), bbox_inches='tight')


def plot_with_pyplot_q3(no_sorting_points, sorting_points, random_points, label):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    x_range = range(MIN_DEPTH, MAX_DEPTH + 1)
    # plt.plot(x_range, no_sorting_points, "o-", label='Minimax')
    # plt.plot(x_range, alphabeta_points, "ro-", label='Alpha-beta')
    plt.plot(x_range, no_sorting_points, "o-", label='No sorting')
    plt.plot(x_range, sorting_points, "ro-", label='Sorting by heuristic')
    plt.plot(x_range, random_points, "go-", label='Random order')
    # plt.title('Question 1{}'.format(label))
    plt.xlabel('Depth cutoff')
    plt.ylabel('Number of states explored')
    plt.grid(True)
    plt.legend()
    # plt.show()

    f.savefig('plots/question3{}.pdf'.format(label), bbox_inches='tight')


def plot_with_pyplot_q5(default_heur_points, random_heur_points, win_heur_points, label):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    x_range = range(MIN_TIME, MAX_TIME + 1)
    # plt.plot(x_range, no_sorting_points, "o-", label='Minimax')
    # plt.plot(x_range, alphabeta_points, "ro-", label='Alpha-beta')
    plt.plot(x_range, default_heur_points, "o-", label='Default heuristic')
    plt.plot(x_range, random_heur_points, "ro-", label='Random number heuristic')
    plt.plot(x_range, win_heur_points, "go-", label='Win/loss heuristic')
    # plt.title('Question 1{}'.format(label))
    plt.xlabel('Time limit (s)')
    plt.ylabel('Number of states explored')
    plt.grid(True)
    plt.legend()
    # plt.show()
    f.savefig('plots/question5{}.pdf'.format(label), bbox_inches='tight')


def plot_with_pyplot_q5b(default_heur_points, random_heur_points, win_heur_points, label):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    x_range = range(MIN_TIME, MAX_TIME + 1)
    # plt.plot(x_range, no_sorting_points, "o-", label='Minimax')
    # plt.plot(x_range, alphabeta_points, "ro-", label='Alpha-beta')
    plt.plot(x_range, default_heur_points, "o-", label='Default heuristic')
    plt.plot(x_range, random_heur_points, "ro-", label='Random number heuristic')
    plt.plot(x_range, win_heur_points, "go-", label='Win/loss heuristic')
    # plt.title('Question 1{}'.format(label))
    plt.xlabel('Time limit (s)')
    plt.ylabel('Maximum depth reached')
    plt.grid(True)
    plt.legend()
    # plt.show()
    f.savefig('plots/question5_depth_{}.pdf'.format(label), bbox_inches='tight')


def question1():
    """
    For each of these configurations, graph the total number of states explored by your program when using depth cutoffs
    of 3, 4, 5 and 6, both with minimax and alpha-beta. Assume it is white's turn to play.
    """
    print('Question 1')
    states = [
        (file_to_state('states/state_q1a.txt'), 'A'),
        (file_to_state('states/state_q1b.txt'), 'B'),
        (file_to_state('states/state_q1c.txt'), 'C')]
    for state, label in states:
        minimax_points, negamax_points = get_searched_states_starting_at(state, label)
        plot_with_pyplot_q1(minimax_points, negamax_points, label)


def question3():
    """
    Explain whether the number of states explored depends on the order in which you generate new states during the
    search. Justify your response using results from your program.
    """
    print('Question 3')
    states = [
        (file_to_state('states/state_q1a.txt'), 'A'),
        (file_to_state('states/state_q1b.txt'), 'B'),
        (file_to_state('states/state_q1c.txt'), 'C')]
    for state, label in states:
        no_sorting_points, sorting_points, random_points = get_searched_states_with_ordering(state, label)
        plot_with_pyplot_q3(no_sorting_points, sorting_points, random_points, label)


def question5():
    """
    A more complex evaluation function will increase computation time. Since each move is time constrained,
    explain whether this favours the use of simpler evaluation functions so that your agent can evaluate nodes deeper
    in the game tree.
    """
    print('Question 5')
    states = [
        (file_to_state('states/state_q1a.txt'), 'A'),
        (file_to_state('states/state_q1b.txt'), 'B'),
        (file_to_state('states/state_q1c.txt'), 'C')]
    for state, label in states:
        default_heur_points, random_heur_points, win_heur_points = get_searched_states_with_heuristics(state, label)
        # plot_with_plotly(minimax_points, alphabeta_points, negamax_points, label).
        plot_with_pyplot_q5(default_heur_points, random_heur_points, win_heur_points, label)


def question5b():
    """
    A more complex evaluation function will increase computation time. Since each move is time constrained,
    explain whether this favours the use of simpler evaluation functions so that your agent can evaluate nodes deeper
    in the game tree.
    """
    states = [
        # (file_to_state('states/state_q1a.txt'), 'A'),
        (file_to_state('states/state_q1b.txt'), 'B'),
        # (file_to_state('states/state_q1c.txt'), 'C')
    ]
    for state, label in states:
        default_heur_points, random_heur_points, win_heur_points = get_searched_states_with_heuristics_and_return_depth(
            state, label)
        # plot_with_plotly(minimax_points, alphabeta_points, negamax_points, label).
        plot_with_pyplot_q5b(default_heur_points, random_heur_points, win_heur_points, label)


def get_minimax_number_states_explored(initial_state, depth):
    transposition_table = {}
    minimax.counter = 0
    val = minimax(initial_state, depth, transposition_table, white_player=True, count=True)
    return minimax.counter, val


def get_alphabeta_number_states_explored(initial_state, depth):
    transposition_table = {}
    alphabeta.counter = 0
    _, val = alphabeta(initial_state, depth, transposition_table, time_limit=10000, start_time=time.time(), alpha=-INF,
                       beta=INF, white_player=True, count=True)
    return alphabeta.counter, val


def iterative_dfs_negamax_states(state, time_limit, depth_limit, white_player, heuristic=default_heuristic):
    start_time = time.time()
    transposition_table = {}
    num_states = 0
    for d in range(depth_limit):
        t = time.time()
        negamax.counter = 0
        best_action, v = negamax(state, d, -INF, INF, transposition_table, time_limit, start_time, 1, True,
                                 heuristic=heuristic)
        num_states += negamax.counter
        if v is None:  # Incomplete search
            return num_states
        elapsed_time = time.time() - t
        print('Depth {}, value: {}, best action: {}, elapsed time: {}, states visited: {}'
              .format(d, v, action_tuple_to_str(best_action), elapsed_time, negamax.counter))
        if white_player and v >= WIN_HEURISTIC or not white_player and v <= -WIN_HEURISTIC:
            print('Win found for {} player with move {}'.format(
                'white' if white_player else 'black',
                action_tuple_to_str(best_action)))
            return num_states
        if time.time() - start_time >= time_limit:
            return num_states
    return num_states


def iterative_dfs_negamax_depth(state, time_limit, depth_limit, white_player, heuristic=default_heuristic):
    start_time = time.time()
    transposition_table = {}
    num_states = 0
    for d in range(depth_limit):
        t = time.time()
        negamax.counter = 0
        best_action, v = negamax(state, d, -INF, INF, transposition_table, time_limit, start_time, 1, True,
                                 heuristic=heuristic)
        num_states += negamax.counter
        if v is None:  # Incomplete search
            return d - 1
        elapsed_time = time.time() - t
        print('Depth {}, value: {}, best action: {}, elapsed time: {}, states visited: {}'
              .format(d, v, action_tuple_to_str(best_action), elapsed_time, negamax.counter))
        if white_player and v >= WIN_HEURISTIC or not white_player and v <= -WIN_HEURISTIC:
            print('Win found for {} player with move {}'.format(
                'white' if white_player else 'black',
                action_tuple_to_str(best_action)))
            return d
        if time.time() - start_time >= time_limit:
            return d
    return depth_limit - 1


def get_iterative_dfs_negamax_number_states_explored(initial_state, depth=DEFAULT_DEPTH, t=DEFAULT_TIME,
                                                     heuristic=default_heuristic):
    num_states = iterative_dfs_negamax_states(initial_state, t, depth, True, heuristic=heuristic)
    return num_states


def get_iterative_dfs_negamax_depth(initial_state, depth=DEFAULT_DEPTH, t=DEFAULT_TIME,
                                    heuristic=default_heuristic):
    depth = iterative_dfs_negamax_depth(initial_state, t, depth, True, heuristic=heuristic)
    return depth


def get_negamax_number_states_explored(initial_state, depth, order=SORTED_BY_HEURISTIC_ORDER,
                                       heuristic=default_heuristic):
    transposition_table = {}
    negamax.counter = 0
    _, val = negamax(initial_state, depth, -INF, INF, transposition_table, 10000, time.time(), 1, count=True,
                     order=order, heuristic=heuristic)
    return negamax.counter, val


def plot_state(state, label):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.tick_top()
    ax.set_xlim([0.5, 7.5])
    ax.set_ylim([7.5, 0.5])
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('gray')
    white_pieces = state[0]
    x_range_white = []
    y_range_white = []
    for x, y in white_pieces:
        x_range_white.append(x)
        y_range_white.append(y)
    black_pieces = state[1]
    x_range_black = []
    y_range_black = []
    for x, y in black_pieces:
        x_range_black.append(x)
        y_range_black.append(y)
    plt.plot(x_range_white, y_range_white, "wo", label='White pieces', ms=15, mew=5)
    plt.plot(x_range_black, y_range_black, "kx", label='Black pieces', ms=15, mew=5)
    plt.grid(True)
    # plt.legend()
    # plt.show()

    f.savefig('plots/state_{}.pdf'.format(label), bbox_inches='tight')


def graph_game_states_abc():
    states = [
        (file_to_state('states/state_q1a.txt'), 'A'),
        (file_to_state('states/state_q1b.txt'), 'B'),
        (file_to_state('states/state_q1c.txt'), 'C')]
    for state, label in states:
        plot_state(state, label)


def graph_game_states_12_moves():
    states = [
        (file_to_state('states/state_random_12_moves.txt'), 'random_12'),
        (file_to_state('states/state_win_loss_12_moves.txt'), 'win_loss_12'),
        (file_to_state('states/state_default_12_moves.txt'), 'default_12')]
    for state, label in states:
        plot_state(state, label)


if __name__ == '__main__':
    # graph_game_states_abc()
    # question1()
    # question3()
    # question5()
    # question5b()
    graph_game_states_12_moves()
