# Quarto game

An adaptation of the quarto board game. It's a strategy game, that is played with 16 different pieces on a 4 x 4 square grid. The goal is to align 4 pieces that share at least one common characteristic. This two player game is played turn by turn. Each turn, a player must choose a piece that the opponent will play. Then the opponent chooses an empty position to play the piece. After each turn, players swap roles: the piece chooser becomes the next position chooser and the position chooser becomes the next piece chooser. The game ends when after choosing a position where to put a piece, there is an alignment of 4 pieces that share at least one common characteristic, or when there are no pieces left.

## Installation
### Requirements
This package has no external dependencies, it is written in pure Python using libraries from the standard library.

### Installation instructions
Clone this repository, then install it using uv: `uv install`. If you don't have uv yet, youcan download it by following the [installation instruction](https://docs.astral.sh/uv/getting-started/installation/)
