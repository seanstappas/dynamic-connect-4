import telnetlib
from argparse import ArgumentParser

import time

from connect_four import file_to_state, print_state, action_str_to_tuple, actions, result, action_tuple_to_str
from heuristics import WIN_HEURISTIC, win_loss_heuristic
from search import iterative_dfs_negamax

DEPTH_LIMIT = 100
TIME_PER_MOVE = '19'


def human_vs_ai(arguments):
    """
    Play a human vs AI game.

    :param arguments: the command-line arguments
    """
    state = file_to_state(arguments.state)
    white_player = True
    human_player = arguments.colour == 'white'
    time_limit = float(arguments.time_limit)
    move_number = 1
    while True:
        print_state(state)

        print('Move number: {}'.format(move_number))

        start_time = time.time()
        if human_player:  # Human player
            state = human_move(state, white_player)
        else:
            state = ai_move(state, white_player, time_limit)
        print('Move time: {} s'.format(time.time() - start_time))

        if abs(win_loss_heuristic(state)) >= WIN_HEURISTIC:
            print_state(state)
            player = 'White' if white_player else 'Black'
            print(player + ' wins!')
            return

        white_player = not white_player
        human_player = not human_player
        move_number += 1


def human_vs_human(arguments):
    """
    Play a human vs human game.

    :param arguments: the command-line arguments
    """
    state = file_to_state(arguments.state)
    white_player = True
    move_number = 1
    while True:
        print_state(state)
        print('Move number: {}'.format(move_number))
        player = 'White' if white_player else 'Black'

        start_time = time.time()
        state = human_move(state, white_player)
        print('Move time: {} s'.format(time.time() - start_time))

        if abs(win_loss_heuristic(state)) >= WIN_HEURISTIC:
            print(player + ' wins!')
            return

        white_player = not white_player
        move_number += 1


def ai_vs_ai(arguments):
    """
    Watch an AI vs AI game.

    :param arguments: the command-line arguments
    """
    state = file_to_state(arguments.state)
    white_player = True
    time_limit = float(arguments.time_limit)
    move_number = 1
    while True:
        print_state(state)
        print('Move number: {}'.format(move_number))

        start_time = time.time()
        state = ai_move(state, white_player, time_limit)
        print('Move time: {} s'.format(time.time() - start_time))

        if abs(win_loss_heuristic(state)) >= WIN_HEURISTIC:
            print_state(state)
            player = 'White' if white_player else 'Black'
            print(player + ' wins!')
            return

        white_player = not white_player
        move_number += 1


def ai_vs_remote(arguments):
    """
    Watch an AI vs remote game.

    :param arguments: the command-line arguments
    """
    state = file_to_state(arguments.state)
    player = arguments.colour
    server_turn = player == 'black'
    tn = setup_telnet(arguments)
    white_player = True
    time_limit = float(arguments.time_limit)
    move_number = 1
    while True:
        print_state(state)
        print('Move number: {}'.format(move_number))

        start_time = time.time()
        if server_turn:
            state = remote_move(tn, state, white_player)
        else:
            state = ai_move(state, white_player, time_limit, tn)
        print('Move time: {} s'.format(time.time() - start_time))

        if abs(win_loss_heuristic(state)) >= WIN_HEURISTIC:
            print_state(state)
            player = 'White' if white_player else 'Black'
            print(player + ' wins!')
            return

        white_player = not white_player
        server_turn = not server_turn
        move_number += 1


def human_vs_remote(arguments):
    """
    Play a human vs remote game.

    :param arguments: the command-line arguments
    """
    state = file_to_state(arguments.state)
    white_player = True
    local_move = arguments.colour == 'white'
    tn = setup_telnet(arguments)
    move_number = 1
    while True:
        print_state(state)
        print('Move number: {}'.format(move_number))
        player = 'White' if white_player else 'Black'

        start_time = time.time()
        if local_move:
            state = human_move(state, white_player, tn)
        else:
            state = remote_move(tn, state, white_player)
        print('Move time: {} s'.format(time.time() - start_time))

        if abs(win_loss_heuristic(state)) >= WIN_HEURISTIC:
            print_state(state)
            print(player + ' wins!')
            return

        white_player = not white_player
        local_move = not local_move
        move_number += 1


def setup_telnet(arguments):
    """
    Setup the telnet local client.

    :param arguments: the command-line arguments
    :return: the telnet client
    """
    host = arguments.host
    port = arguments.port
    colour = arguments.colour
    game_id = arguments.game_id

    print('Establishing connection to host {}, port {}...'.format(host, port))
    tn = telnetlib.Telnet(host, port)

    print('Sending game information (game ID: {}, colour: {})...'.format(game_id, colour))
    tn.write('{} {}\n'.format(game_id, colour))

    print('Waiting for opponent to join game with ID {}...'.format(game_id))
    tn.read_until(game_id)

    print("Starting game with ID '{}'!".format(game_id))
    return tn


def remote_move(tn, state, white_player):
    """
    Wait for a move from a remote player.

    :param tn: the telnet client
    :param state: the current state
    :param white_player: True if it is white's turn to make a move, False otherwise
    :return: the resulting state after applying the remote player's move
    """
    string_move = None
    print('Waiting for move from remote player...')
    while action_str_to_tuple(string_move) not in actions(state, white_player):
        string_move = tn.read_until('\n')
    action = action_str_to_tuple(string_move)
    print('{} (server) move: {}'.format('White' if white_player else 'Black', string_move))
    return result(state, action, white_player)


def ai_move(state, white_player, time_limit, tn=None):
    """
    Wait for a move from the local AI.

    :param state: the current state
    :param white_player: True if it is white's turn to make a move, False otherwise
    :param time_limit: the time limit for a move
    :param tn: the telnet client. Ignored if None.
    :return: the resulting state after applying the AI's move.
    """
    player = 'White' if white_player else 'Black'
    best_action = iterative_dfs_negamax(state, time_limit, DEPTH_LIMIT, white_player)
    print('{} (AI) move: {}'.format(player, action_tuple_to_str(best_action)))
    if tn is not None:
        tn.write(action_tuple_to_str(best_action) + '\n')
    return result(state, best_action, white_player)


def human_move(state, white_player, tn=None):
    """
    Wait for a move from the human player.

    :param state: the current state
    :param white_player: True if it is white's turn to make a move, False otherwise
    :param tn: the telnet client. Ignored if None.
    :return: the resulting state after applying the human's move.
    """
    player = 'White' if white_player else 'Black'
    invalid_move = True
    while invalid_move:
        invalid_move = False
        move = raw_input(player + ', enter your move:\n')
        action = action_str_to_tuple(move)
        if action not in actions(state, white_player):
            print('Invalid move.')
            invalid_move = True
        else:
            if tn is not None:
                tn.write(action_tuple_to_str(action) + '\n')
            print('{} (human) move: {}'.format(player, action_tuple_to_str(action)))
            state = result(state, action, white_player)
    return state


if __name__ == '__main__':
    practice_address = 'ai.anassinator.com'
    local_address = 'localhost'

    test_state = 'states/test_state_Sep23.txt'
    initial_state = 'states/initial_state.txt'


    def add_server_arguments(p):
        p.add_argument('-H', '--host', default=local_address, help='Server host address.')
        p.add_argument('-p', '--port', type=int, default=12345, help='Port number.')
        p.add_argument('-g', '--game_id', default='game_id', help="Game ID.")


    def add_state_argument(p):
        p.add_argument('-s', '--state', default=initial_state, help='The name of the file containing the '
                                                                    'initial state of the game.')

    def add_color_argument(p):
        p.add_argument('-c', '--colour', default='white', help='Your colour.')


    def add_local_ai_arguments(p):
        p.add_argument('-t', '--time_limit', default=TIME_PER_MOVE, help='The time limit for a move, in seconds.')


    parser = ArgumentParser(description='Dynamic Connect-4. To play or watch a game, use one of the positional '
                                        'arguments.')
    subparsers = parser.add_subparsers()

    parser_hvh = subparsers.add_parser('human_vs_human', help='Play as a human versus another human.')
    parser_hvh.set_defaults(func=human_vs_human)
    add_state_argument(parser_hvh)

    parser_hva = subparsers.add_parser('human_vs_ai', help='Play as a human versus an AI.')
    parser_hva.set_defaults(func=human_vs_ai)
    add_state_argument(parser_hva)
    add_color_argument(parser_hva)
    add_local_ai_arguments(parser_hva)

    parser_ava = subparsers.add_parser('ai_vs_ai', help='Spectate an AI versus AI game.')
    parser_ava.set_defaults(func=ai_vs_ai)
    add_state_argument(parser_ava)
    add_local_ai_arguments(parser_ava)

    parser_avs = subparsers.add_parser('ai_vs_server', help='Spectate an AI versus a player on a server.')
    add_server_arguments(parser_avs)
    add_state_argument(parser_avs)
    add_color_argument(parser_avs)
    add_local_ai_arguments(parser_avs)
    parser_avs.set_defaults(func=ai_vs_remote)

    parser_hvs = subparsers.add_parser('human_vs_server', help='Play as a human versus a player on a server.')
    add_server_arguments(parser_hvs)
    add_state_argument(parser_hvs)
    add_color_argument(parser_hvs)
    parser_hvs.set_defaults(func=human_vs_remote)

    # args = parser.parse_args('human_vs_human'.split())
    # args = parser.parse_args('human_vs_ai'.split())
    # args = parser.parse_args('ai_vs_ai'.split())
    # args = parser.parse_args('ai_vs_server'.split())
    # args = parser.parse_args('human_vs_server'.split())
    args = parser.parse_args()
    args.func(args)
