# src/heuristics.py

"""
Heuristic evaluation functions for Othello.
"""

from board import Board

# Position weights for strategic squares
# Corners are most valuable, edges are good, positions next to corners are bad
POSITION_WEIGHTS = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, 5, 1, 1, 5, -2, 10],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [5, -2, 1, 1, 1, 1, -2, 5],
    [10, -2, 5, 1, 1, 5, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]


def evaluate_position(board: Board, player: int) -> float:
    """
    Main heuristic evaluation function.

    Combines multiple strategic factors:
    1. Coin parity (piece count difference)
    2. Mobility (available moves)
    3. Corner occupancy
    4. Positional weights (corners good, near-corners bad)
    5. Stability (pieces that can't be flipped)

    Returns positive score if player is ahead, negative if behind.
    """
    if board.is_terminal():
        winner = board.get_winner()
        if winner == player:
            return 10000
        elif winner == board.get_opponent(player):
            return -10000
        else:
            return 0  # Draw

    opponent = board.get_opponent(player)

    # 1. Coin parity (less important early game, more important late game)
    player_pieces = board.get_piece_count(player)
    opponent_pieces = board.get_piece_count(opponent)
    total_pieces = player_pieces + opponent_pieces

    # Coin parity matters more in endgame
    game_progress = total_pieces / (board.size * board.size)
    coin_parity = (player_pieces - opponent_pieces) * (10 * game_progress)

    # 2. Mobility (number of legal moves)
    player_moves = len(board.get_legal_moves(player))
    opponent_moves = len(board.get_legal_moves(opponent))

    if player_moves + opponent_moves != 0:
        mobility = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
    else:
        mobility = 0

    # 3. Corner occupancy (corners are extremely valuable)
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    player_corners = sum(1 for r, c in corners if board.board[r][c] == player)
    opponent_corners = sum(1 for r, c in corners if board.board[r][c] == opponent)

    if player_corners + opponent_corners != 0:
        corner_score = 100 * (player_corners - opponent_corners) / (player_corners + opponent_corners)
    else:
        corner_score = 0

    # 4. Positional weights
    positional_score = 0
    for r in range(board.size):
        for c in range(board.size):
            if board.board[r][c] == player:
                positional_score += POSITION_WEIGHTS[r][c]
            elif board.board[r][c] == opponent:
                positional_score -= POSITION_WEIGHTS[r][c]

    # 5. Stability (pieces that cannot be flipped)
    player_stable = count_stable_discs(board, player)
    opponent_stable = count_stable_discs(board, opponent)

    if player_stable + opponent_stable != 0:
        stability = 100 * (player_stable - opponent_stable) / (player_stable + opponent_stable)
    else:
        stability = 0

    # Weighted combination
    # Early game: prioritize mobility and position
    # Late game: prioritize coin parity
    if game_progress < 0.5:
        score = (
                coin_parity * 1.0 +
                mobility * 3.0 +
                corner_score * 5.0 +
                positional_score * 2.0 +
                stability * 2.0
        )
    else:
        score = (
                coin_parity * 5.0 +
                mobility * 2.0 +
                corner_score * 8.0 +
                positional_score * 1.5 +
                stability * 3.0
        )

    return score


def count_stable_discs(board: Board, player: int) -> int:
    """
    Count stable discs (pieces that cannot be flipped).
    A disc is stable if it's in a corner or adjacent to stable discs in all directions.
    Simplified version: only count corners and edge pieces adjacent to corners.
    """
    stable = 0

    # Corners are always stable if occupied
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for r, c in corners:
        if board.board[r][c] == player:
            stable += 1

    # Edges adjacent to occupied corners are somewhat stable
    # This is a simplified stability metric
    corner_regions = [
        [(0, 0), [(0, 1), (1, 0)]],
        [(0, 7), [(0, 6), (1, 7)]],
        [(7, 0), [(6, 0), (7, 1)]],
        [(7, 7), [(6, 7), (7, 6)]]
    ]

    for corner, adjacents in corner_regions:
        if board.board[corner[0]][corner[1]] == player:
            for r, c in adjacents:
                if board.board[r][c] == player:
                    stable += 0.5

    return stable


def evaluate_simple(board: Board, player: int) -> float:
    """
    Simpler heuristic for comparison/ablation testing.
    Only uses coin parity and corner control.
    """
    if board.is_terminal():
        winner = board.get_winner()
        if winner == player:
            return 10000
        elif winner == board.get_opponent(player):
            return -10000
        else:
            return 0

    opponent = board.get_opponent(player)

    # Coin difference
    coin_diff = board.get_piece_count(player) - board.get_piece_count(opponent)

    # Corner control
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    player_corners = sum(1 for r, c in corners if board.board[r][c] == player)
    opponent_corners = sum(1 for r, c in corners if board.board[r][c] == opponent)
    corner_diff = player_corners - opponent_corners

    return coin_diff * 10 + corner_diff * 100

