# Quarto game

An adaptation of the quarto board game. It's a strategy game, that is played with 16 different pieces on a 4 x 4 square grid. The goal is to align 4 pieces that share at least one common characteristic. This two player game is played turn by turn. Each turn, a player must choose a piece that the opponent will play. Then the opponent chooses an empty position to play the piece. After each turn, players swap roles: the piece chooser becomes the next position chooser and the position chooser becomes the next piece chooser. The game ends when after choosing a position where to put a piece, there is an alignment of 4 pieces that share at least one common characteristic, or when there are no pieces left.

## Installation
### Requirements
This package has only a dependency to the `tqdm` package, used to show progress bars when running benchmarks. Otherwise, it is written in pure Python using libraries from the standard library.

### Installation instructions
Clone this repository, then install it using uv: `uv venv` to create a virtual environment, then `uv pip install` . If you don't have uv yet, you can download it by following the [installation instruction](https://docs.astral.sh/uv/getting-started/installation/)

## Game modes
You can play in three modes: 
* human vs human
* human vs machine
* machine vs machine
See the relevant functions in `game.py`
To start a new game against a machine (by default at level 2), run `main.py`

## Robot strategy
There will be four increasing difficulty modes for the machine. Each level applies strategy from the lower levels if the current strategy is not applicable. Currently levels 0, 1 and 2 are implemented.
* At level 0, the machine chooses pieces and position randomly
* At level 1, when given a winning piece, the machine will find a position that wins the game.
* At level 2, when possible the machine will avoid giving the opponent a winning piece. 
* At level 3 (not implemented yet), when choosing a position, the machine will try to find a position, such that it can give a non winning piece next turn.


## Benchmark
There can be robot battles! Currently the winrate of the robots playing against themselves are the following (on a 10000 games average, given as win rate / loss rate / tie rate):
|         | level 0    | level 1    | level 2     |
|---------|------------|------------|-------------|
| level 0 | 49%/49%/2% | n/a        | n/a         |
| level 1 | 90%/10%/0% | 50%/50%/0% | n/a         |
| level 2 | 98%/2%/0%  | 90%/10%/0% | 49%/50%/1%  |