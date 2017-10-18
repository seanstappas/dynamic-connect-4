# Dynamic Connect-4

This is a Python implementation of an agent that can play the Dynamic Connect-4 game. This is assignment 1 of the ECSE-526 class, as described [here](http://www.cim.mcgill.ca/~jer/courses/ai/assignments/as1.html).

The agent uses a flavour of alpha-beta pruning with transposition table and heuristic function to search the state space and pick the best move.

## Play

To play the game, use the command-line interface in `main.py`. To see the list of available commands, run the following:

```
python main.py --help
```

This will print the following, summarizing the ways of playing or watching the game:

```
usage: main.py [-h]
               {human_vs_human,human_vs_ai,ai_vs_ai,ai_vs_server,human_vs_server}
               ...

Dynamic Connect-4. To play or watch a game, use one of the positional
arguments.

positional arguments:
  {human_vs_human,human_vs_ai,ai_vs_ai,ai_vs_server,human_vs_server}
    human_vs_human      Play as a human versus another human.
    human_vs_ai         Play as a human versus an AI.
    ai_vs_ai            Spectate an AI versus AI game.
    ai_vs_server        Spectate an AI versus a player on a server.
    human_vs_server     Play as a human versus a player on a server.

optional arguments:
  -h, --help            show this help message and exit
```

### Optional Arguments

#### State

To manually specify a state, use the following argument:

```
  -s STATE, --state STATE
                        The name of the file containing the initial state of
                        the game.
```

Note that the command expects a file with state in the following format:

```
 , , , , , ,X
X, , , , , ,O
O, , , , , ,X
X, , , , , ,O
O, , , , , ,X
X, , , , , ,O
O, , , , , ,
```

Note that if the initial state is not specified, the program assumes that there is a `states` directory (at the same level as `main.py`) containing an `initial_state.txt` file.

#### Colour

When playing any game mode besides `human_vs_human` or `ai_vs_ai`, your colour must be specified.

```
  -c COLOUR, --colour COLOUR
                        Your colour.
```

#### Time Limit

When playing with a local AI agent (with `human_vs_ai`, `ai_vs_ai` or `ai_vs_server`), the time limit for a move can be set:

```
  -t TIME_LIMIT, --time_limit TIME_LIMIT
                        The time limit for a move, in seconds.
```

#### Remote Play Arguments

When playing remotely (either with `ai_vs_server` or `human_vs_server`), there is the following set of optional arguments:

```
  -H HOST, --host HOST  Server host address.
  -p PORT, --port PORT  Port number.
  -g GAME_ID, --game_id GAME_ID
                        Game ID.
```

#### Default Values

All of the optional arguments above have default values, if none are provided by the user. Here are these default values:

Argument | Default Value
--- | ---
`--colour` | `white`
`--state` | `states/initial_state.txt`
`--time_limit` | `19`
`--host` | `localhost`
`--port` | `12345`
`--game_id` | `game_id`

A sample log of the output of the program (when using the `ai_vs_ai` mode) can be seen in `logs/sample_log.txt`.

### Example Commands

Here are some example commands:

```
python main.py ai_vs_server -H localhost -p 12345 -g game_id_123 -t 19 -c white
```

```
python main.py ai_vs_ai -t 10
```

```
python main.py human_vs_human -c white
```

## Code Organization

There are four main Python files that contain the bulk of the program code, outlined in the following table:

File | Contents
--- | ---
`connect_four.py` | State, board and action information.
`heuristics.py` | Heuristics tested or used by the program.
`search.py` | Search methods, including minimax, negamax and iterative deepening search.
`main.py` | Main method to parse command-line arguments and execute the game.

The files with prefix `test` were used to test various aspects of the game, and the `graph_creator.py` script was used to create the graphs for the assignment report, alongside the MATLAB scripts in the `matlab` directory.
