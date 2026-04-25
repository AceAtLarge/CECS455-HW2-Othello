# src/game.py

"""
Othello game loop and rendering.
"""

import time
from typing import Optional, Tuple
from board import Board
from agents import Agent


class Game:
    """Manages the Othello game loop."""

    def __init__(self, player1: Agent, player2: Agent, time_limit: float = 1.0):
        """
        Initialize game.

        Args:
            player1: Agent for BLACK (player 1)
            player2: Agent for WHITE (player 2)
            time_limit: Time limit per move in seconds
        """
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.time_limit = time_limit
        self.move_count = 0

    def play(self, verbose: bool = True) -> Optional[int]:
        """
        Play a complete game.

        Args:
            verbose: If True, print board after each move

        Returns:
            Winner (Board.BLACK, Board.WHITE, or None for draw)
        """
        consecutive_passes = 0

        while not self.board.is_terminal():
            if verbose:
                print("\n" + "=" * 50)
                print(f"Move {self.move_count + 1}")
                print(self.board)

            current_player = self.board.current_player
            agent = self.player1 if current_player == Board.BLACK else self.player2

            legal_moves = self.board.get_legal_moves(current_player)

            if not legal_moves:
                # Player must pass
                if verbose:
                    player_name = "BLACK (X)" if current_player == Board.BLACK else "WHITE (O)"
                    print(f"\n{player_name} has no legal moves and must pass.")

                self.board.current_player = self.board.get_opponent(current_player)
                consecutive_passes += 1

                # Game ends if both players pass consecutively
                if consecutive_passes >= 2:
                    break

                continue

            consecutive_passes = 0

            # Get move from agent
            if verbose:
                player_name = "BLACK (X)" if current_player == Board.BLACK else "WHITE (O)"
                print(f"\n{player_name} ({agent.name}) is thinking...")

            start_time = time.perf_counter()
            move = agent.get_move(self.board, self.time_limit)
            elapsed = time.perf_counter() - start_time

            if move is None:
                if verbose:
                    print(f"ERROR: {agent.name} returned None despite having legal moves!")
                break

            # Validate and make move
            if not self.board.is_legal_move(move[0], move[1], current_player):
                if verbose:
                    print(f"ERROR: {agent.name} made illegal move {move}!")
                break

            self.board.make_move(move[0], move[1], current_player)
            self.move_count += 1

            if verbose:
                print(f"Move: {move}, Time: {elapsed:.3f}s")
                if hasattr(agent, 'nodes_visited'):
                    print(f"Nodes visited: {agent.nodes_visited}, Max depth: {agent.max_depth_reached}")

        # Game over
        if verbose:
            print("\n" + "=" * 50)
            print("GAME OVER")
            print(self.board)

        winner = self.board.get_winner()

        if verbose:
            if winner == Board.BLACK:
                print("\nWinner: BLACK (X)")
            elif winner == Board.WHITE:
                print("\nWinner: WHITE (O)")
            else:
                print("\nResult: DRAW")

            print(f"Final score - X: {self.board.get_piece_count(Board.BLACK)}, "
                  f"O: {self.board.get_piece_count(Board.WHITE)}")

        return winner


class HumanPlayer(Agent):
    """Human player that gets input from command line."""

    def __init__(self):
        super().__init__("Human")

    def get_move(self, board: Board, time_limit: float) -> Optional[Tuple[int, int]]:
        legal_moves = board.get_legal_moves(board.current_player)

        if not legal_moves:
            return None

        print(f"\nLegal moves: {legal_moves}")

        while True:
            try:
                user_input = input("Enter your move as 'row col' (e.g., '3 4'): ").strip()
                parts = user_input.split()

                if len(parts) != 2:
                    print("Invalid format. Please enter two numbers separated by space.")
                    continue

                row, col = int(parts[0]), int(parts[1])

                if (row, col) not in legal_moves:
                    print(f"Illegal move. Choose from: {legal_moves}")
                    continue

                return (row, col)

            except ValueError:
                print("Invalid input. Please enter two integers.")
            except KeyboardInterrupt:
                print("\nGame interrupted by user.")
                return None


