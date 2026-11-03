import random
import subprocess
import sys
from pathlib import Path

import pytest

import rubik
from cube import RubikCube

HERE = Path(__file__).parent
SOLVED = "yyyyrrrrwwwwppppbbbbgggg"
ALL_MOVES = sorted(rubik.MOVES)


@pytest.fixture(scope="module", autouse=True)
def precalculated():
    if not rubik.preSolutionCubes:
        rubik.preCalcCubes()


def is_solved(cube):
    return rubik.checkSolved(cube) == (True, "")


def test_default_cube_matches_solved_text():
    assert RubikCube().get_key() == RubikCube(SOLVED).get_key()


def test_parsing_is_case_insensitive():
    assert RubikCube(SOLVED.upper()).get_key() == RubikCube(SOLVED).get_key()


@pytest.mark.parametrize("text", ["yyyy", SOLVED + "y", "x" + SOLVED[1:]])
def test_invalid_state_raises(text):
    with pytest.raises(ValueError):
        RubikCube(text)


def test_copy_is_independent():
    cube = RubikCube()
    clone = cube.copy()
    clone.move_left_down()
    assert cube.get_key() == RubikCube().get_key()
    assert clone.get_key() != cube.get_key()


@pytest.mark.parametrize("move", ALL_MOVES)
def test_move_changes_state_and_has_order_four(move):
    cube = RubikCube()
    rubik.applyMoves(cube, move)
    assert cube.get_key() != RubikCube().get_key()
    rubik.applyMoves(cube, move * 3)
    assert cube.get_key() == RubikCube().get_key()


@pytest.mark.parametrize("move", ALL_MOVES)
def test_move_is_undone_by_its_inverse(move):
    cube = RubikCube()
    rubik.applyMoves(cube, "lTf")
    before = cube.get_key()
    rubik.applyMoves(cube, move + move.swapcase())
    assert cube.get_key() == before


def test_moves_keep_four_stickers_per_color():
    cube = RubikCube()
    rubik.applyMoves(cube, "lFtLaBrT")
    stickers = [s for side in cube.cube for row in side for s in row]
    assert sorted(stickers.count(color) for color in set(stickers)) == [4] * 6


def test_whole_cube_rotation_keeps_cube_solved():
    cube = RubikCube()
    rubik.applyMoves(cube, "tB")  # top and bottom layer turned the same way
    assert is_solved(cube)


def test_24_solved_orientations():
    cubes = {}
    rubik.calculateDefaultCubesOriented(cubes)
    assert len(cubes) == 24


def test_precalculation_size():
    # 24 orientations expanded by LEVEL_OF_PRECALCULATION = 4 moves
    assert len(rubik.preSolutionCubes) == 16512


def test_solved_cube_needs_no_moves():
    assert rubik.findSolution(RubikCube()) == ""


def test_known_hard_scramble():
    cube = rubik.applyMoves(RubikCube(), "ttlfTlFlFTLL")
    solution = rubik.findSolution(cube)
    assert solution
    assert is_solved(rubik.applyMoves(cube, solution))


@pytest.mark.parametrize("seed", range(5))
def test_random_scrambles_are_solved(seed):
    random.seed(seed)
    cube = rubik.random_moves(RubikCube(), 8)
    solution = rubik.findSolution(cube)
    assert solution is not None
    assert is_solved(rubik.applyMoves(cube, solution))


def test_solve_prints_solution(capsys):
    rubik.solve(rubik.applyMoves(RubikCube(), "lf"))
    assert "Found Solution: FL" in capsys.readouterr().out


def test_cli_solves_state_from_argument():
    result = subprocess.run([sys.executable, str(HERE / "rubik.py"), "rgrggpyybbppwwbrwwgpyyrb"],
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 0
    solution = result.stdout.split("Found Solution: ")[1].split()[0]
    assert is_solved(rubik.applyMoves(RubikCube("rgrggpyybbppwwbrwwgpyyrb"), solution))


def test_cli_rejects_invalid_state():
    result = subprocess.run([sys.executable, str(HERE / "rubik.py"), "abc"],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode != 0
    assert "24 color letters" in result.stderr
