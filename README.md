# HW2: Othello

Details

# HW: Othello with Minimax

## Overview

Build a **playable** Othello game where:

-   A human can play against your AI **or** the AI can play itself.
    
-   Your AI chooses moves with **minimax** (alpha–beta optional but encouraged).
    
-   The AI must respect a **per-move time limit** in seconds.
    

Design your **own heuristic evaluation** for non-terminal positions. The fun bit: making it _play smart_ under time pressure.

---

## Learning goals

1.  Implement complete [**game rules** Links to an external site.](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english) and legal move generation.
    
2.  Use **minimax** (with optional **alpha–beta**) and **iterative deepening** under a time budget.
    
3.  Design, measure, and defend a **heuristic evaluation**.
    
4.  Build a **human-playable** loop and a **self-play** harness.
    

---

## The game

-   [https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english Links to an external site.](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english)
    

---

## Program requirements

### CLI

Your program must support:

`python main.py --mode [human-ai | ai-ai] --seconds 2.0 --ai1 <AgentA> --ai2 <AgentB> --first [1|2]`

-   `--seconds S` = **per-move time limit** (float seconds).
    
-   `--mode human-ai` → human plays as Player 1 by default (toggle with `--first`).
    
-   `--mode ai-ai` → run self-play matches (useful for grading).
    
-   `--ai1/--ai2` = agent class names (e.g., `RandomAgent`, `MinimaxAgent`).
    

### Time control (must-have)

-   Use **iterative deepening**: search depth 1, 2, 3, … until time expires; return the **best fully evaluated move** so far.
    
-   Provide the agent with either:
    
    -   a callable `time_remaining() -> float` in seconds, **or**
        
    -   a hard deadline timestamp `deadline = now + S`.
        
-   If the deadline hits mid-search, **immediately** return the best move from the last completed depth.
    
-   If no move was completed (shouldn’t happen unless S≈0), pick any legal move.
    

### Architecture (suggested)

`board.py # board state, legal moves, apply/undo, terminal detection, winner`

`agents.py # base Agent, RandomAgent (baseline), MinimaxAgent (yours)`

`heuristics.py # your evaluation function(s)`

`game.py # game loop (human/AI, AI/AI), rendering (ASCII or lightweight GUI)`

`main.py # CLI wiring`

---

## Minimax (with optional alpha–beta)

**Required:** minimax with **iterative deepening** and a **heuristic** for non-terminal nodes.  
**Optional (extra credit):** alpha–beta pruning.

**Alpha–beta tip:** Order moves “center-first” to prune more in Othello.

---

## Heuristic design (you choose!)

You must craft and justify a static evaluation `score(board)` from the perspective of the current player. Ideas:

-   **Number of coins**
-   **Number of moves possible**
-   **Number of pieces immune to turning**
-   **Corner control:** assign points to control of each of the four corners of the board.
    
-   **Near-corner scoring:** placing coins directly next to the four corners might give the corner to the other player, so weigh them negatively.
    
-   **Immediate win/loss checks:** +/-∞ (handled as terminal).
    

---

## Rendering

-   **ASCII** is fine (print board after each move).
    
-   Optional: lightweight GUI (e.g., Pygame). Don’t let the UI block the search thread if you run timers.
    

---

## Baselines (include these)

-   `RandomAgent`: chooses a random legal column.
    
-   `Greedy1PlyAgent` (optional but helpful for testing): pick the move with the highest heuristic after 1 ply (no opponent response).
    

Your `MinimaxAgent` should **consistently beat `RandomAgent`** under the same time limit.

---

## Correctness checks (must pass)

1.  **Rules**: no illegal moves; correct gravity; correct win detection in all directions.
    
2.  **Draw**: full board → draw.
    
3.  **Time**: never exceed the per-move time by more than ~50ms (tolerance).
    
4.  **Determinism**: with a fixed random seed for tie-breaks, same position → same move.
    

---

## Experiments to run (report in write-up)

1.  **Strength vs baselines:** 50 games vs `RandomAgent` (25 starting first, 25 second) at `--seconds 1.0`. Report win/draw/loss.
    
2.  **Heuristic ablation:** briefly compare two versions of your heuristic (e.g., with/without center weighting).
    
3.  **Search depth vs time:** log average completed depth and nodes/second at 0.25s, 0.5s, 1.0s per move.
    
4.  **Alpha–beta (if used):** report average nodes visited vs plain minimax (same positions, same ordering).
    

---

## Deliverables

-   Code (see structure above).
    
    -   Submission modalities:
        
        -   -   In order to grade your assignment efficiently, I have to be able to run your assignment without major effort.
            -   For this reason, the following languages and document formats are excluded and will not be allowed under any circumstances. **Submitting your assignment in any of these will result in a grade of zero**:
                -   Languages: APL, COBOL, JOVIAL, Prolog.
                -   Formats: Jupyter Notebook (too cumbersome to set up and work with).
                -   IDE dependency: Code that can only be compiled and/or run from within a specific IDE.
                -   OS or architecture dependency: Code that can only be compiled and/or run on one OS or only one specific architecture (e.g., x64 or ARM).
                -   Any language or format that can only be used, read, debugged etc. to the full extent using software that is only commercially available and not provided by CSULB free of charge to students.
-   `README.md`: how to run human vs AI and AI vs AI; flags; any dependencies.
    
-   `writeup.pdf` (≤2 pages):
    
    -   Explain your heuristic, weights, and why they make sense for Othello.
        
    -   Summarize experiment results (tables/plots welcome).
        
    -   Note edge cases you handled (full columns, simultaneous wins not possible, etc.).
        

---

## Grading (20 pts + 3 extra credit)

-   **Game correctness (rules, terminal detection, legal moves): 6**
    
-   **Time-aware minimax (iterative deepening; respects deadline): 4**
    
-   **Heuristic quality & agent strength: 4**
    
    -   Beats `RandomAgent` in majority of games; sensible evaluation design & justification.
        
-   **Code quality (structure, clarity, comments, small functions, no blocking UI): 4**
    
-   **Write-up (clarity, experiments, insight): 2**
    
-   **Extra credit for alpha-beta pruning: 3**
    -   **Must be clearly commented in the code**

---

---

## Testing checklist

-   Drop into full columns → rejected.
    
-   Horizontal/vertical/diagonal wins detected.
    
-   Time = 0.1s still returns a move reliably (iterative deepening works).
    
-   Self-play (`ai-ai`) runs to completion with consistent results under a fixed seed.
    

---

## Tips

-   Use **`time.perf_counter()`** for deadlines.
    
-   Always keep the **best move from the last fully completed depth**.
    
-   Start move ordering from the **center column outward** to boost alpha–beta pruning.
    
-   Keep your heuristic **fast**—you’ll call it millions of times.
    
