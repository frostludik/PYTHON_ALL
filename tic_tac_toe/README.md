# tic_tac_toe
Project 2 for Engeto Python online academy


## Overview

This script implements a command-line version of the classic Tic-Tac-Toe game. It allows two players to play against each other, taking turns to place their marks (X or O) on a 3x3 grid. The game continues until one player wins or the board is full, resulting in a draw.

## Features

- **Two-Player Mode**: Allows two players to play against each other.
- **Turn-Based Gameplay**: Players take turns to place their marks on the grid.
- **Win Detection**: Detects when a player has won by getting three of their marks in a row, column, or diagonal.
- **Draw Detection**: Detects when the game is a draw if the board is full and no player has won.
- **Input Validation**: Ensures that players can only place their marks on empty cells and within the valid range.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

## Usage

Run the script using Python:
```sh
python tic_tac_toe.py
```

## How to Play

### Start the Game

- Run the script to start the game.
- The game will display an empty 3x3 grid.

### Player Turns

- Players take turns to enter the row and column number where they want to place their mark (X or O).
- The game will update the grid and display it after each turn.

### Winning the Game

- The game will detect if a player has won by getting three of their marks in a row, column, or diagonal.
- The game will announce the winner and end.

### Draw

- If the board is full and no player has won, the game will declare a draw and end.
