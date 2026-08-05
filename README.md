# pyRubik2x2

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A solver for the 2x2 Rubik's Cube — also known as the **Pocket Cube** or **Mini Cube** — running entirely in the terminal with a colored ANSI rendering of the cube.

![Screenshot](screenshot.png)

## How it works

The solver combines a **breadth-first search** with a **pre-calculation step**:

1. All 24 orientations of the solved cube are generated as target states.
2. From those targets, every state reachable within `LEVEL_OF_PRECALCULATION` moves (default: `4`) is enumerated and cached.
3. A BFS from the scrambled state runs until it meets the cached set.

Meeting in the middle roughly halves the effective search depth, which keeps the state space tractable without shipping a full pattern database.

## Requirements

- Python 3.9 or newer — no third-party dependencies
- A terminal with ANSI color support

## Installation

```bash
git clone https://github.com/michaelkrisper/pyRubik2x2.git
cd pyRubik2x2
```

Nothing to build or install.

## Usage

### Interactive mode

```bash
python3 rubik.py
```

Opens a prompt where you can turn faces manually, randomize the cube, and ask for a solution.

### Solve a given state

```bash
python3 rubik.py <cube-state>
```

Passes the cube state directly as an argument; the solver prints the move sequence that returns it to solved.

## Project structure

| File | Purpose |
|---|---|
| `rubik.py` | Entry point — interactive loop, pre-calculation, BFS solver |
| `cube.py` | `RubikCube` class — state representation, rotations, rendering |
| `run.bat` | Convenience launcher for Windows |

## License

MIT — see [LICENSE](LICENSE).
