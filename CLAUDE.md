# CLAUDE.md

Terminal solver for the 2x2 Rubik's Cube (Pocket Cube) with ANSI-colored rendering.
Python 3.9+, standard library only; no packaging, nothing deployed. `run.bat` is a
Windows launcher.

## Commands

```bash
python3 rubik.py                              # interactive mode
python3 rubik.py yyyyrrrrwwwwppppbbbbgggg     # solve a 24-letter state and exit
pip install pytest ruff
pytest                                        # test_rubik.py, ~4 s (pre-calculation)
ruff check                                    # ruff.toml: E, F, W, I, UP (UP031 off); 120 cols
```

CI (`.github/workflows/ci.yml`) runs ruff on 3.14 and pytest on 3.9 to 3.14.

## Architecture

- `cube.py`: `RubikCube`, state as `cube[face][row][col]` (faces top, front, bottom,
  back, left, right) holding ANSI sticker strings; the 12 `move_*` methods, parsing of
  the 24-letter state (`y r w p b g`, case-insensitive, `ValueError` on bad input),
  `get_key()` and `print_cube()`.
- `rubik.py`: CLI and solver. `preCalcCubes()` fills the global `preSolutionCubes`
  with the 24 orientations of the solved cube plus everything within
  `LEVEL_OF_PRECALCULATION` (4) moves, in a background thread started by `main()`.
  `findSolution()` runs a BFS from the input until it hits that table, then appends the
  stored path inverted. `MOVES` maps letters to method names.
- The solver only turns `l L t T f F`; the other faces are covered by the 24 target
  orientations.

## Rules and pitfalls

- Copy cubes with `cube.copy()`. Never rebuild one from `get_key()`: the key is the
  joined ANSI strings, not the 24-letter input format.
- A move letter and its inverse differ only in case; `checkSolved()` inverts stored
  paths with `swapcase()[::-1]`. Keep that pairing when adding or remapping moves.
- Anything that solves must wait for the pre-calculation (`t.join()` in `main()`);
  tests call `rubik.preCalcCubes()` once in a module fixture.
- Raising `LEVEL_OF_PRECALCULATION` grows memory and start-up time quickly; solutions
  are short but not guaranteed optimal.
- `rubik.py` uses legacy camelCase, `cube.py` snake_case; match the file you edit.
  Stay on the 3.9 syntax level and standard library only.

## Workflow

- Every change starts with a GitHub issue. Branch `<issue>-<slug>` from `main`,
  open a PR with `Closes #<issue>`. Never push to `main` directly.
- PRs auto-merge (squash) once CI and the "Linked ticket" check pass; drafts are not merged.
- Versions exist only as git tags `vX.Y.Z`. Every merge to `main` tags the next patch;
  never edit version numbers in files. Minor/major releases: Actions -> Release.
- Nothing is deployed; a merge to `main` only creates the patch tag.
- Details: CONTRIBUTING.md.
