# src/board.py

"""
Othello board implementation with complete game rules.
"""

from typing import List, Tuple, Optional, Set
from copy import deepcopy


class Board:
    """Represents an Othello game board."""

    EMPTY = 0
    BLACK = 1
    WHITE = 2

    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    def __init__(self, size: int = 8):
        """Initialize an 8x8 Othello board with starting position."""
        self.size = size
        self.board = [[self.EMPTY for _ in range(size)] for _ in range(size)]

        # Standard starting position
        mid = size // 2
        self.board[mid - 1][mid - 1] = self.WHITE
        self.board[mid - 1][mid] = self.BLACK
        self.board[mid][mid - 1] = self.BLACK
        self.board[mid][mid] = self.WHITE

        self.current_player = self.BLACK
        self.move_history = []

    def copy(self) -> 'Board':
        """Create a deep copy of the board."""
        new_board = Board.__new__(Board)
        new_board.size = self.size
        new_board.board = deepcopy(self.board)
        new_board.current_player = self.current_player
        new_board.move_history = self.move_history.copy()
        return new_board

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= row < self.size and 0 <= col < self.size

    def get_opponent(self, player: int) -> int:
        """Get the opponent's color."""
        return self.WHITE if player == self.BLACK else self.BLACK

    def would_flip_in_direction(self, row: int, col: int, dr: int, dc: int, player: int) -> List[Tuple[int, int]]:
        """
        Check if placing a piece at (row, col) would flip pieces in direction (dr, dc).
        Returns list of positions that would be flipped.
        """
        opponent = self.get_opponent(player)
        flipped = []

        r, c = row + dr, col + dc

        # Must have at least one opponent piece in this direction
        while self.is_valid_position(r, c) and self.board[r][c] == opponent:
            flipped.append((r, c))
            r += dr
            c += dc

        # Must end with player's piece (and have flipped at least one opponent piece)
        if flipped and self.is_valid_position(r, c) and self.board[r][c] == player:
            return flipped

        return []

    def is_legal_move(self, row: int, col: int, player: int) -> bool:
        """Check if a move is legal for the given player."""
        if not self.is_valid_position(row, col):
            return False

        if self.board[row][col] != self.EMPTY:
            return False

        # Check if this move flips any pieces in any direction
        for dr, dc in self.DIRECTIONS:
            if self.would_flip_in_direction(row, col, dr, dc, player):
                return True

        return False

    def get_legal_moves(self, player: int) -> List[Tuple[int, int]]:
        """Get all legal moves for the given player."""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_legal_move(row, col, player):
                    moves.append((row, col))
        return moves

    def make_move(self, row: int, col: int, player: int) -> bool:
        """
        Make a move on the board. Returns True if successful.
        Flips all appropriate pieces.
        """
        if not self.is_legal_move(row, col, player):
            return False

        # Place the piece
        self.board[row][col] = player

        # Flip pieces in all valid directions
        all_flipped = []
        for dr, dc in self.DIRECTIONS:
            flipped = self.would_flip_in_direction(row, col, dr, dc, player)
            all_flipped.extend(flipped)

        for r, c in all_flipped:
            self.board[r][c] = player

        # Record move
        self.move_history.append((row, col, player, all_flipped))

        # Switch player
        self.current_player = self.get_opponent(player)

        return True

    def is_terminal(self) -> bool:
        """Check if the game is over (no legal moves for either player)."""
        return (len(self.get_legal_moves(self.BLACK)) == 0 and
                len(self.get_legal_moves(self.WHITE)) == 0)

    def get_winner(self) -> Optional[int]:
        """
        Get the winner of the game.
        Returns BLACK, WHITE, or None for a draw.
        Only valid when game is terminal.
        """
        if not self.is_terminal():
            return None

        black_count = sum(row.count(self.BLACK) for row in self.board)
        white_count = sum(row.count(self.WHITE) for row in self.board)

        if black_count > white_count:
            return self.BLACK
        elif white_count > black_count:
            return self.WHITE
        else:
            return None  # Draw

    def get_piece_count(self, player: int) -> int:
        """Count pieces for a given player."""
        return sum(row.count(player) for row in self.board)

    def __str__(self) -> str:
        """ASCII representation of the board."""
        symbols = {self.EMPTY: '.', self.BLACK: 'X', self.WHITE: 'O'}

        lines = []
        lines.append("  " + " ".join(str(i) for i in range(self.size)))
        for i, row in enumerate(self.board):
            lines.append(f"{i} " + " ".join(symbols[cell] for cell in row))

        black_count = self.get_piece_count(self.BLACK)
        white_count = self.get_piece_count(self.WHITE)
        lines.append(f"\nX (Black): {black_count}  O (White): {white_count}")

        return "\n".join(lines)


