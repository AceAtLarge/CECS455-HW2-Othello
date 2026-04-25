# Othello with Minimax AI

A complete implementation of Othello with AI agents using minimax search with alpha-beta pruning and iterative deepening.

## Features

- ✅ Complete Othello game rules implementation
- ✅ Minimax search with alpha-beta pruning
- ✅ Iterative deepening with time control
- ✅ Multiple AI agents (Random, Greedy, Minimax)
- ✅ Human vs AI and AI vs AI modes
- ✅ Strategic heuristic evaluation function
- ✅ ASCII board rendering

## Requirements

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

## Installation

No installation required. Simply clone or download the files and run:

```bash
python main.py --mode human-ai
```

## Usage

### Basic Command Format

```bash
python main.py --mode [human-ai | ai-ai] --seconds <time> --ai1 <agent> --ai2 <agent> --first [1|2]
```

### Arguments

- `--mode`: Game mode
  - `human-ai`: Human vs AI
  - `ai-ai`: AI vs AI (for testing/tournaments)

- `--seconds`: Time limit per move in seconds (default: 1.0)
  - Example: `--seconds 2.5`

- `--ai1`: Agent for Player 1 (BLACK) in ai-ai mode (default: MinimaxAgent)
  - Available: `MinimaxAgent`, `RandomAgent`, `Greedy1PlyAgent`, `MinimaxAgent_NoAB`

- `--ai2`: Agent for Player 2 (WHITE) (default: RandomAgent)
  - Same options as ai1

- `--first`: Which player goes first (default: 1)
  - `1`: Player 1 (BLACK) goes first
  - `2`: Player 2 (WHITE) goes first
  - In human-ai mode, determines if human plays as BLACK or WHITE

- `--quiet`: Suppress output (useful for batch testing)

### Example Usages

#### 1. Human vs AI (Human plays as BLACK)
```bash
python main.py --mode human-ai --seconds 1.0
```

#### 2. Human vs AI (Human plays as WHITE)
```bash
python main.py --mode human-ai --seconds 1.0 --first 2
```

#### 3. AI vs AI (Minimax vs Random)
```bash
python main.py --mode ai-ai --seconds 1.0 --ai1 MinimaxAgent --ai2 RandomAgent
```

#### 4. AI vs AI (Two Minimax agents with different time limits)
```bash
python main.py --mode ai-ai --seconds 0.5 --ai1 MinimaxAgent --ai2 MinimaxAgent
```

#### 5. Quiet mode (no output, for batch testing)
```bash
python main.py --mode ai-ai --seconds 1.0 --quiet
```

## How to Play (Human Mode)

When it's your turn, you'll see:
1. The current board state
2. List of legal moves as (row, col) coordinates
3. Prompt to enter your move

Enter your move as two numbers separated by space:
```
Enter your move as 'row col' (e.g., '3 4'): 3 4
```

Board coordinates:
- Rows: 0-7 (top to bottom)
- Cols: 0-7 (left to right)
- X = BLACK (Player 1)
- O = WHITE (Player 2)
- . = Empty

## File Structure

```
.
├── main.py          # CLI entry point and argument parsing
├── game.py          # Game loop and human player interface
├── board.py         # Board state, legal moves, game rules
├── agents.py        # AI agents (Random, Minimax, Greedy)
├── heuristics.py    # Evaluation functions
├── test_othello.py  # Tests
└── README.md        # This file
```

## AI Implementation Details

### Minimax Agent

The `MinimaxAgent` uses:

1. **Iterative Deepening**: Searches depth 1, 2, 3, ... until time runs out
2. **Alpha-Beta Pruning**: Reduces nodes explored by ~50-90%
3. **Time Control**: Respects hard deadline using `time.perf_counter()`
4. **Move Ordering**: Center-first ordering for better pruning

### Heuristic Evaluation

The evaluation function combines multiple strategic factors:

1. **Coin Parity** (10-50 points): Piece count difference
   - More important in late game
   
2. **Mobility** (0-100 points): Number of legal moves
   - More important in early game
   
3. **Corner Control** (0-100 points): Corners are extremely valuable
   - Corners cannot be flipped
   
4. **Positional Weights**: Strategic square values
   - Corners: +100
   - Near-corners: -20 to -50 (dangerous, can give corners away)
   - Edges: +10
   - Center: +5
   
5. **Stability** (0-100 points): Pieces that cannot be flipped
   - Simplified metric based on valueable corners and edge pieces

The weights are adjusted based on game progress (early vs late game).


## Testing

Run a quick test match:

```bash
# Minimax should consistently beat Random
python main.py --mode ai-ai --seconds 1.0 --ai1 MinimaxAgent --ai2 RandomAgent

# Test with shorter time limit
python main.py --mode ai-ai --seconds 0.25 --ai1 MinimaxAgent --ai2 RandomAgent
```


## Credits

Implements the official Othello rules from the World Othello Federation.
Architecture suggested from Professor.

