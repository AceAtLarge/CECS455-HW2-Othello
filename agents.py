# src/agents.py

"""
AI agents for Othello.
"""

import random
import time
from typing import Tuple, Optional, Callable
from board import Board
from heuristics import evaluate_position


class Agent:
    """Base class for Othello agents."""

    def __init__(self, name: str):
        self.name = name

    def get_move(self, board: Board, time_limit: float) -> Optional[Tuple[int, int]]:
        """
        Get the agent's move given a board state and time limit.

        Args:
            board: Current board state
            time_limit: Time limit in seconds for this move

        Returns:
            (row, col) tuple or None if no legal moves
        """
        raise NotImplementedError


class RandomAgent(Agent):
    """Agent that chooses random legal moves."""

    def __init__(self):
        super().__init__("RandomAgent")

    def get_move(self, board: Board, time_limit: float) -> Optional[Tuple[int, int]]:
        legal_moves = board.get_legal_moves(board.current_player)
        if not legal_moves:
            return None
        return random.choice(legal_moves)


class Greedy1PlyAgent(Agent):
    """Agent that picks the move with highest immediate heuristic value."""

    def __init__(self):
        super().__init__("Greedy1PlyAgent")

    def get_move(self, board: Board, time_limit: float) -> Optional[Tuple[int, int]]:
        legal_moves = board.get_legal_moves(board.current_player)
        if not legal_moves:
            return None

        best_move = None
        best_score = float('-inf')

        for move in legal_moves:
            # Simulate move
            test_board = board.copy()
            test_board.make_move(move[0], move[1], board.current_player)
            score = evaluate_position(test_board, board.current_player)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move


class MinimaxAgent(Agent):
    """
    Agent using minimax with alpha-beta pruning and iterative deepening
    """

    def __init__(self, use_alpha_beta: bool = True):
        name = "MinimaxAgent" + ("_AB" if use_alpha_beta else "")
        super().__init__(name)
        self.use_alpha_beta = use_alpha_beta
        self.nodes_visited = 0
        self.max_depth_reached = 0

    def get_move(self, board: Board, time_limit: float) -> Optional[Tuple[int, int]]:
        """Get move using iterative deepening minimax."""
        legal_moves = board.get_legal_moves(board.current_player)
        if not legal_moves:
            return None

        if len(legal_moves) == 1:
            return legal_moves[0]

        # Setup time control
        deadline = time.perf_counter() + time_limit

        best_move = legal_moves[0]  # Fallback
        self.nodes_visited = 0
        self.max_depth_reached = 0

        # Iterative deepening
        depth = 1
        while True:
            # Check if we have time for another iteration
            time_remaining = deadline - time.perf_counter()
            if time_remaining < 0.01:  # Safety margin
                break

            try:
                move, score = self._search_depth(
                    board,
                    depth,
                    board.current_player,
                    deadline
                )

                if move is not None:
                    best_move = move
                    self.max_depth_reached = depth

                # Checks if we're out of time
                if time.perf_counter() >= deadline:
                    break

                depth += 1

                # Stop if we've searched deep enough (game is nearly solved)
                if depth > 20:
                    break

            except TimeoutError:
                # Time expired during search
                break

        return best_move

    def _search_depth(self, board: Board, max_depth: int, player: int, deadline: float) -> Tuple[
        Optional[Tuple[int, int]], float]:
        """
        Search to a fixed depth and return best move and score.
        """
        legal_moves = board.get_legal_moves(player)
        if not legal_moves:
            return None, 0

        # Order moves: center-first for better alpha-beta pruning
        legal_moves = self._order_moves(legal_moves, board.size)

        best_move = legal_moves[0]
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in legal_moves:
            # Check timeout
            if time.perf_counter() >= deadline:
                raise TimeoutError()

            # Make move
            new_board = board.copy()
            new_board.make_move(move[0], move[1], player)

            # Minimax with alpha-beta
            if self.use_alpha_beta:
                score = self._minimax_ab(
                    new_board,
                    max_depth - 1,
                    False,
                    player,
                    alpha,
                    beta,
                    deadline
                )
            else:
                score = self._minimax(
                    new_board,
                    max_depth - 1,
                    False,
                    player,
                    deadline
                )

            if score > best_score:
                best_score = score
                best_move = move

            # Alpha-beta update here
            if self.use_alpha_beta:
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cutoff

        return best_move, best_score

    def _minimax(self, board: Board, depth: int, is_maximizing: bool,
                 player: int, deadline: float) -> float:
        """Minimax without alpha-beta pruning."""
        self.nodes_visited += 1

        # Check timeout
        if time.perf_counter() >= deadline:
            raise TimeoutError()

        # Terminal or depth limit
        if depth == 0 or board.is_terminal():
            return evaluate_position(board, player)

        current_player = board.current_player
        legal_moves = board.get_legal_moves(current_player)

        # Pass if no legal moves
        if not legal_moves:
            new_board = board.copy()
            new_board.current_player = board.get_opponent(current_player)
            return self._minimax(new_board, depth - 1, not is_maximizing, player, deadline)

        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = board.copy()
                new_board.make_move(move[0], move[1], current_player)
                eval = self._minimax(new_board, depth - 1, False, player, deadline)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = board.copy()
                new_board.make_move(move[0], move[1], current_player)
                eval = self._minimax(new_board, depth - 1, True, player, deadline)
                min_eval = min(min_eval, eval)
            return min_eval

    def _minimax_ab(self, board: Board, depth: int, is_maximizing: bool,
                    player: int, alpha: float, beta: float, deadline: float) -> float:
        """Minimax with alpha-beta pruning."""
        self.nodes_visited += 1

        # Check timeout
        if time.perf_counter() >= deadline:
            raise TimeoutError()

        # Terminal or depth limit
        if depth == 0 or board.is_terminal():
            return evaluate_position(board, player)

        current_player = board.current_player
        legal_moves = board.get_legal_moves(current_player)

        # Pass if no legal moves
        if not legal_moves:
            new_board = board.copy()
            new_board.current_player = board.get_opponent(current_player)
            return self._minimax_ab(new_board, depth - 1, not is_maximizing,
                                    player, alpha, beta, deadline)

        # Order moves for better pruning
        legal_moves = self._order_moves(legal_moves, board.size)

        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = board.copy()
                new_board.make_move(move[0], move[1], current_player)
                eval = self._minimax_ab(new_board, depth - 1, False,
                                        player, alpha, beta, deadline)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = board.copy()
                new_board.make_move(move[0], move[1], current_player)
                eval = self._minimax_ab(new_board, depth - 1, True,
                                        player, alpha, beta, deadline)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def _order_moves(self, moves: list, board_size: int) -> list:
        """
        Order moves with center-first strategy for better alpha-beta pruning.
        In Othello, center positions are often more valuable early.
        """
        center = board_size / 2

        def distance_from_center(move):
            r, c = move
            return abs(r - center) + abs(c - center)

        return sorted(moves, key=distance_from_center)


