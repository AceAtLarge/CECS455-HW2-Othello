# src/test_othello.py

"""
Quick test script to verify Othello implementation.
"""

from board import Board
from agents import RandomAgent, MinimaxAgent, Greedy1PlyAgent
from game import Game
import time


def test_board_basics():
    """Test basic board operations."""
    print("Testing board basics...")

    board = Board()

    # Check initial position
    assert board.board[3][3] == Board.WHITE
    assert board.board[3][4] == Board.BLACK
    assert board.board[4][3] == Board.BLACK
    assert board.board[4][4] == Board.WHITE

    # Check initial legal moves for BLACK
    legal_moves = board.get_legal_moves(Board.BLACK)
    assert len(legal_moves) == 4  # Should have 4 legal opening moves

    print("✓ Board initialization correct")
    print("✓ Legal move generation working")


def test_move_execution():
    """Test making moves."""
    print("\nTesting move execution...")

    board = Board()
    legal_moves = board.get_legal_moves(Board.BLACK)

    # Make first legal move
    move = legal_moves[0]
    success = board.make_move(move[0], move[1], Board.BLACK)
    assert success

    # Check player switched
    assert board.current_player == Board.WHITE

    print("✓ Move execution working")
    print("✓ Player switching working")


def test_game_termination():
    """Test that games can complete."""
    print("\nTesting game completion...")

    game = Game(RandomAgent(), RandomAgent(), time_limit=0.1)
    winner = game.play(verbose=False)

    # Winner should be BLACK, WHITE, or None (draw)
    assert winner in [Board.BLACK, Board.WHITE, None]

    print("✓ Game completes successfully")
    print(f"✓ Winner: {'BLACK' if winner == Board.BLACK else 'WHITE' if winner == Board.WHITE else 'DRAW'}")


def test_minimax_agent():
    """Test that minimax agent works."""
    print("\nTesting Minimax agent...")

    agent = MinimaxAgent(use_alpha_beta=True)
    board = Board()

    start = time.perf_counter()
    move = agent.get_move(board, time_limit=1.0)
    elapsed = time.perf_counter() - start

    assert move is not None
    assert move in board.get_legal_moves(Board.BLACK)
    assert elapsed < 1.1  # Should respect time limit (with small margin)

    print(f"✓ Minimax found move: {move}")
    print(f"✓ Time used: {elapsed:.3f}s")
    print(f"✓ Nodes visited: {agent.nodes_visited}")
    print(f"✓ Max depth: {agent.max_depth_reached}")


def test_minimax_vs_random():
    """Test Minimax vs Random (should win most games)."""
    print("\nTesting Minimax vs Random (3 games)...")

    wins = 0
    for i in range(3):
        game = Game(MinimaxAgent(use_alpha_beta=True), RandomAgent(), time_limit=0.5)
        winner = game.play(verbose=False)
        if winner == Board.BLACK:
            wins += 1
        print(
            f"  Game {i + 1}: {'Minimax wins' if winner == Board.BLACK else 'Random wins' if winner == Board.WHITE else 'Draw'}")

    print(f"✓ Minimax won {wins}/3 games")


def test_time_limits():
    """Test various time limits."""
    print("\nTesting different time limits...")

    agent = MinimaxAgent(use_alpha_beta=True)
    board = Board()

    for time_limit in [0.1, 0.25, 0.5, 1.0]:
        start = time.perf_counter()
        move = agent.get_move(board, time_limit)
        elapsed = time.perf_counter() - start

        assert move is not None
        assert elapsed < time_limit + 0.1  # Small tolerance

        print(f"  {time_limit}s limit: {elapsed:.3f}s used, depth {agent.max_depth_reached}")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("OTHELLO IMPLEMENTATION TESTS")
    print("=" * 60)

    try:
        test_board_basics()
        test_move_execution()
        test_game_termination()
        test_minimax_agent()
        test_minimax_vs_random()
        test_time_limits()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise


if __name__ == '__main__':
    run_all_tests()

