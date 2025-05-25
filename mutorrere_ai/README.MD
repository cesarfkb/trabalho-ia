# Mutorere (Traditional Māori Game)

Mutorere is a traditional Māori board game for two players. This project is a digital implementation of the game.

## Game Rules

### 1. Counters

- Each player controls **four counters**, called _perepere_. There are white and black pieces.

### 2. The Board

- The board consists of **eight outer points** (_kewai_) arranged in a circle, and **one central point** (_pūtahi_).

### 3. Setup

- At the start of the game:
  - Each player places their four counters on **four consecutive kewai**.
  - The _pūtahi_ (center) is left empty.

### 4. Turns & Movement

- Players take turns, alternating between each other.
- On each turn, a player must:
  - Move one of their counters to an **empty adjacent point**.
  - Movement is allowed only to **directly connected (adjacent) points**.
  - A counter may move to the _pūtahi_ (center) **only if it is adjacent to an opponent's counter**.

### 5. Objective

- The winner is the player who **blocks all of the opponent's counters**, leaving them with no legal moves.

### 6. Additional Notes

- Counters **cannot jump over other counters**.
- Only **one counter may occupy a point at any time**.

---

## Project Structure

- `main.py` — Entry point, runs the game loop
- `board.py` — Board drawing and state logic
- `game.py` — Game rules, turn management, win conditions
- `player.py` — Player logic (human/AI)
- `pieces.py` — Piece/counter logic (optional)
- `mutorrere.py` — Ruleset and documentation

## Getting Started

Instructions for running the game will be added as development progresses.

---

_For more information on Mutorere, see [Wikipedia](https://en.wikipedia.org/wiki/Mutorere)._
