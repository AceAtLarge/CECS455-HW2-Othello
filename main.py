# src/main.py

"""
Main entry point for Othello game with CLI.
"""

import argparse
import sys
from board import Board
from agents import RandomAgent, MinimaxAgent, Greedy1PlyAgent
from game import Game, HumanPlayer


def get_agent(agent_name: str):
    """Create an agent instance from a name."""
    agents = {
        'RandomAgent': RandomAgent,
        'MinimaxAgent': lambda: MinimaxAgent(use_alpha_beta=True),
        'MinimaxAgent_NoAB': lambda: MinimaxAgent(use_alpha_beta=False),
        'Greedy1PlyAgent': Greedy1PlyAgent,
        'Human': HumanPlayer
    }

    if agent_name not in agents:
        print(f"Unknown agent: {agent_name}")
        print(f"Available agents: {', '.join(agents.keys())}")
        sys.exit(1)

    return agents[agent_name]()


def main():
    parser = argparse.ArgumentParser(description='Play Othello with AI')

    parser.add_argument('--mode', type=str, required=True,
                        choices=['human-ai', 'ai-ai'],
                        help='Game mode: human-ai or ai-ai')

    parser.add_argument('--seconds', type=float, default=1.0,
                        help='Time limit per move in seconds (default: 1.0)')

    parser.add_argument('--ai1', type=str, default='MinimaxAgent',
                        help='Agent for player 1 (BLACK) in ai-ai mode (default: MinimaxAgent)')

    parser.add_argument('--ai2', type=str, default='RandomAgent',
                        help='Agent for player 2 (WHITE) (default: RandomAgent)')

    parser.add_argument('--first', type=int, default=1, choices=[1, 2],
                        help='Which player goes first (1=BLACK, 2=WHITE). In human-ai mode, '
                             'determines if human is player 1 or 2 (default: 1)')

    parser.add_argument('--verbose', action='store_true', default=True,
                        help='Print board after each move (default: True)')

    parser.add_argument('--quiet', action='store_true',
                        help='Suppress output (overrides --verbose)')

    args = parser.parse_args()

    # Determine verbosity
    verbose = args.verbose and not args.quiet

    # Create agents based on mode
    if args.mode == 'human-ai':
        if args.first == 1:
            # Human is BLACK (player 1)
            player1 = HumanPlayer()
            player2 = get_agent(args.ai2)
            if verbose:
                print(f"Human (BLACK) vs {args.ai2} (WHITE)")
        else:
            # Human is WHITE (player 2)
            player1 = get_agent(args.ai1)
            player2 = HumanPlayer()
            if verbose:
                print(f"{args.ai1} (BLACK) vs Human (WHITE)")

    elif args.mode == 'ai-ai':
        player1 = get_agent(args.ai1)
        player2 = get_agent(args.ai2)
        if verbose:
            print(f"{args.ai1} (BLACK) vs {args.ai2} (WHITE)")

    if verbose:
        print(f"Time limit: {args.seconds} seconds per move\n")

    # Play game
    game = Game(player1, player2, time_limit=args.seconds)
    winner = game.play(verbose=verbose)

    # Return exit code based on result (useful for automated testing)
    if winner == Board.BLACK:
        sys.exit(1)  # Player 1 won
    elif winner == Board.WHITE:
        sys.exit(2)  # Player 2 won
    else:
        sys.exit(0)  # Draw


if __name__ == '__main__':
    main()


