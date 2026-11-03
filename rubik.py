#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
This script provides a solver for the 2x2 Rubik's Cube (Pocket Cube).

It can be run interactively to allow manual manipulation of the cube,
randomization, and solving. It can also solve a cube state provided as a
command-line argument.

The solver uses a breadth-first search algorithm and a pre-calculation step
to find solutions for cubes that are a few moves away from the solved state.
"""
import random
import sys
import threading

from cube import RubikCube

try:
    import readline  # noqa: F401 - enables line editing in input()
except ImportError:
    pass

# CONSTANTS ###################################################################
LEVEL_OF_PRECALCULATION = 4
MOVES = {
    "l": "move_left_down", "L": "move_left_up",
    "t": "move_top_left", "T": "move_top_right",
    "f": "move_front_clockwise", "F": "move_front_anti_clockwise",
    "R": "move_right_down", "r": "move_right_up",
    "B": "move_bottom_left", "b": "move_bottom_right",
    "a": "move_back_clockwise", "A": "move_back_anti_clockwise",
}
# CONSTANTS ###################################################################


# GLOBALS #####################################################################
preSolutionCubes = {}
# GLOBALS #####################################################################


def calculateDefaultCubesOriented(cubes):
    """
    Generates the 24 possible orientations of a solved cube.

    This function populates the `cubes` dictionary with all 24 orientations
    of a solved cube, which are used as the base states for pre-calculation.

    Args:
        cubes (dict): A dictionary to store the pre-calculated cube states.
    """
    c = RubikCube()
    c_copy = c.copy()
    c_copy.move_top_left()
    c_copy.move_bottom_left()
    ctb = c_copy

    c_copy = ctb.copy()
    c_copy.move_top_left()
    c_copy.move_bottom_left()
    ctbtb = c_copy

    c_copy = ctbtb.copy()
    c_copy.move_top_left()
    c_copy.move_bottom_left()
    ctbtbtb = c_copy

    cubes[c.get_key()] = (c, "")
    cubes[ctb.get_key()] = (ctb, "")
    cubes[ctbtb.get_key()] = (ctbtb, "")
    cubes[ctbtbtb.get_key()] = (ctbtbtb, "")

    for cube_obj in [c, ctb, ctbtb, ctbtbtb]:
        for method1, method2 in [("move_right_down", "move_left_down"),
                                 ("move_front_clockwise", "move_back_clockwise")]:
            nextCube = cube_obj
            for _ in range(3):
                c_copy = nextCube.copy()
                getattr(c_copy, method1)()
                getattr(c_copy, method2)()
                nextCube = c_copy
                cubes[nextCube.get_key()] = (nextCube, "")


def checkSolved(testCube):
    """
    Checks if a cube is solved by looking it up in the pre-calculated table.

    Args:
        testCube (RubikCube): The cube to check.

    Returns:
        tuple: A tuple containing a boolean indicating if the cube is solved
               and the path to solve it if it is.
    """
    key = testCube.get_key()
    if key in preSolutionCubes:
        path = preSolutionCubes[key][1]
        return (True, path.swapcase()[::-1])
    else:
        return (False, "")

def getAllMoves(currCube, path):
    """
    Generates all possible next moves for a given cube.

    This function yields a new cube state and the corresponding move for each
    of the 6 possible moves from the current state.

    Args:
        currCube (RubikCube): The current state of the cube.
        path (str): The sequence of moves taken to reach the current state.

    Yields:
        tuple: A tuple containing the new cube state and the updated path.
    """
    if (len(path) == 0 or path[-1] != "L") and (len(path) < 3 or path[-3:] != "lll"):
        new_cube = currCube.copy()
        new_cube.move_left_down()
        yield (new_cube, path + "l")
    if (len(path) == 0 or path[-1] != "T") and (len(path) < 3 or path[-3:] != "ttt"):
        new_cube = currCube.copy()
        new_cube.move_top_left()
        yield (new_cube, path + "t")
    if (len(path) == 0 or path[-1] != "F") and (len(path) < 3 or path[-3:] != "fff"):
        new_cube = currCube.copy()
        new_cube.move_front_clockwise()
        yield (new_cube, path + "f")
    if (len(path) == 0 or path[-1] != "l") and (len(path) < 3 or path[-3:] != "LLL"):
        new_cube = currCube.copy()
        new_cube.move_left_up()
        yield (new_cube, path + "L")
    if (len(path) == 0 or path[-1] != "t") and (len(path) < 3 or path[-3:] != "TTT"):
        new_cube = currCube.copy()
        new_cube.move_top_right()
        yield (new_cube, path + "T")
    if (len(path) == 0 or path[-1] != "f") and (len(path) < 3 or path[-3:] != "FFF"):
        new_cube = currCube.copy()
        new_cube.move_front_anti_clockwise()
        yield (new_cube, path + "F")


def findSolution(inputCube):
    """
    Finds a solution for the given Rubik's Cube using a breadth-first search.

    The search expands states from the input cube until it reaches a state
    from the pre-calculated table, then appends the stored path in reverse.

    Args:
        inputCube (RubikCube): The cube to solve.

    Returns:
        str: The move sequence ("" if already solved), or None if the state
             is unsolvable or the search was interrupted.
    """
    solved, solvePath = checkSolved(inputCube)
    if solved:
        return solvePath
    cubeKeys = {inputCube.get_key()}
    newcubes = [(inputCube, "")]
    try:
        while newcubes:
            cubes, newcubes = newcubes, []
            for currCube, path in cubes:
                for nextCube, nextPath in getAllMoves(currCube, path):
                    key = nextCube.get_key()
                    if key not in cubeKeys:
                        solved, solvePath = checkSolved(nextCube)
                        if solved:
                            return nextPath + solvePath
                        cubeKeys.add(key)
                        newcubes.append((nextCube, nextPath))
    except KeyboardInterrupt:
        pass
    return None


def solve(inputCube):
    """
    Solves the given Rubik's Cube and prints the solution.

    Args:
        inputCube (RubikCube): The cube to solve.
    """
    solution = findSolution(inputCube)
    if solution is None:
        print("\nNo solution found.\n")
    elif solution == "":
        print("\nThe Cube is already solved. Nothing to do.\n")
    else:
        print("\nFound Solution: %s\n" % solution)


def random_moves(cube, count):
    """
    Applies a number of random moves to the cube.

    Args:
        cube (RubikCube): The cube to randomize.
        count (int): The number of random moves to apply.

    Returns:
        RubikCube: The randomized cube.
    """
    cubeKeys = set([cube.get_key()])
    randomMoves = 0
    moves = ["move_left_down", "move_left_up", "move_right_down", "move_right_up",
             "move_top_left", "move_top_right", "move_bottom_left", "move_bottom_right",
             "move_front_clockwise", "move_front_anti_clockwise", "move_back_clockwise", "move_back_anti_clockwise"]
    while randomMoves < count:
        move_name = random.choice(moves)
        getattr(cube, move_name)()
        key = cube.get_key()
        if key not in cubeKeys:
            cubeKeys.add(key)
            randomMoves += 1

    return cube

def applyMoves(cube, moves):
    """
    Applies a sequence of move letters (see MOVES) to the cube in place.

    Args:
        cube (RubikCube): The cube to manipulate.
        moves (str): The move sequence, e.g. "lFtL".

    Returns:
        RubikCube: The same cube, for chaining.
    """
    for move in moves:
        getattr(cube, MOVES[move])()
    return cube


def preCalcCubes():
    """
    Pre-calculates solutions for cubes up to a certain depth.

    This function populates the `preSolutionCubes` dictionary with solutions
    for all cubes that can be solved within `LEVEL_OF_PRECALCULATION` moves.
    """
    calculateDefaultCubesOriented(preSolutionCubes)
    for _ in range(LEVEL_OF_PRECALCULATION):
        for key, (cube, path) in list(preSolutionCubes.items())[:]:
            for nextCube, nextPath in getAllMoves(cube, path):
                key = nextCube.get_key()
                if key not in preSolutionCubes:
                    preSolutionCubes[key] = (nextCube, nextPath)

def main():
    """
    The main function of the Rubik's Cube solver.

    This function handles command-line arguments, starts the pre-calculation
    thread, and enters the interactive command loop.
    """
    t = threading.Thread(target=preCalcCubes)
    t.start()

    print("-- Rubik 2x2 Solver --")

    if sys.argv[1:]:
        try:
            cube = RubikCube(sys.argv[1])
        except ValueError as error:
            sys.exit(str(error))
        cube.print_cube()
        print("Solving...")
        t.join()
        solve(cube)
    else:
        cube = RubikCube("yyyyrrrrwwwwppppbbbbgggg")
        cube.print_cube()
        while True:
            try:
                cmdText = input("Please enter command: ")
            except EOFError:
                sys.exit(0)
            if cmdText == "solve":
                t.join()
                solve(cube)
            elif cmdText == "print":
                cube.print_cube()
            elif cmdText == "random":
                random_moves(cube, 8)
                cube.print_cube()
            elif cmdText == "random4":
                random_moves(cube, 4)
                cube.print_cube()
            elif cmdText == "reset":
                cube = RubikCube()
                cube.print_cube()
            elif cmdText.startswith("init "):
                try:
                    cube = RubikCube(cmdText[5:])
                except ValueError as error:
                    print(error)
                    continue
                cube.print_cube()
            elif cmdText == "exit":
                sys.exit(0)
            elif cmdText != "" and set(cmdText).issubset(set(MOVES)):
                applyMoves(cube, cmdText)
                cube.print_cube()
            else:
                print("Command not known. Possible commands are: solve, print, random, random4, reset, init <state>, "
                      "l, L, t, T, f, F, R, r, B, b, a, A, exit")

if __name__ == "__main__":
    main()
