"""
Tic Tac Toe Player
"""

import math
from typing import List, Optional, Tuple

X = "X"
O = "O"
EMPTY = None

def initial_state() -> List[List[Optional[str]]]:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board: List[List[Optional[str]]]) -> str:
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

def actions(board: List[List[Optional[str]]]) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

def result(board: List[List[Optional[str]]], action: Tuple[int, int]) -> List[List[Optional[str]]]:
    """
    Returns the board that results from making move (i, j) on the board.
    Raises ValueError for invalid moves.
    """
    if not (0 <= action[0] < 3 and 0 <= action[1] < 3):
        raise ValueError("Invalid move: out of bounds")
    
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid move: cell already occupied")
    
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board: List[List[Optional[str]]]) -> Optional[str]:
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None

def terminal(board: List[List[Optional[str]]]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board: List[List[Optional[str]]]) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_result = winner(board)
    if winner_result == X:
        return 1
    elif winner_result == O:
        return -1
    else:
        return 0

def minimax(board: List[List[Optional[str]]]) -> Optional[Tuple[int, int]]:
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    best_score = float('-inf') if current_player == X else float('inf')
    best_action = None

    for action in actions(board):
        try:
            new_board = result(board, action)
            if current_player == X:
                score = min_value(new_board)
                if score > best_score:
                    best_score = score
                    best_action = action
            else:
                score = max_value(new_board)
                if score < best_score:
                    best_score = score
                    best_action = action
        except ValueError:
            continue

    return best_action

def max_value(board: List[List[Optional[str]]]) -> int:
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        try:
            v = max(v, min_value(result(board, action)))
        except ValueError:
            continue
    return v

def min_value(board: List[List[Optional[str]]]) -> int:
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        try:
            v = min(v, max_value(result(board, action)))
        except ValueError:
            continue
    return v