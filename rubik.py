#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This script provides a solver for the 2x2 Rubik's Cube (Pocket Cube).

It can be run interactively to allow manual manipulation of the cube,
randomization, and solving. It can also solve a cube state provided as a
command-line argument.

The solver uses a breadth-first search algorithm and a pre-calculation step
to find solutions for cubes that are a few moves away from the solved state.
"""
import sys
import random
import threading
from cube import RubikCube

try:
    import readline
except ImportError:
    pass

# CONSTANTS ###################################################################
LEVEL_OF_PRECALCULATION = 4
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
    c_copy = RubikCube(c.get_key())
    c_copy.move_top_left()
    c_copy.move_bottom_left()
    ctb = c_copy

    c_copy = RubikCube(ctb.get_key())
    c_copy.move_top_left()
    c_copy.move_bottom_left()
    ctbtb = c_copy

    c_copy = RubikCube(ctbtbtb.get_key())
    c_copy.move_top_left()
    c_copy.move_bottom_left()
    ctbtbtb = c_copy

    cubes[c.get_key()] = (c, "")
    cubes[ctb.get_key()] = (ctb, "")
    cubes[ctbtb.get_key()] = (ctbtb, "")
    cubes[ctbtbtb.get_key()] = (ctbtbtb, "")

    for cube_obj in [c, ctb, ctbtb, ctbtbtb]:
        for method1, method2 in [("move_right_down", "move_left_down"), ("move_front_clockwise", "move_back_clockwise")]:
            nextCube = cube_obj
            for _ in range(3):
                c_copy = RubikCube(nextCube.get_key())
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
        new_cube = RubikCube(currCube.get_key())
        new_cube.move_left_down()
        yield (new_cube, path + "l")
    if (len(path) == 0 or path[-1] != "T") and (len(path) < 3 or path[-3:] != "ttt"):
        new_cube = RubikCube(currCube.get_key())
        new_cube.move_top_left()
        yield (new_cube, path + "t")
    if (len(path) == 0 or path[-1] != "F") and (len(path) < 3 or path[-3:] != "fff"):
        new_cube = RubikCube(currCube.get_key())
        new_cube.move_front_clockwise()
        yield (new_cube, path + "f")
    if (len(path) == 0 or path[-1] != "l") and (len(path) < 3 or path[-3:] != "LLL"):
        new_cube = RubikCube(currCube.get_key())
        new_cube.move_left_up()
        yield (new_cube, path + "L")
    if (len(path) == 0 or path[-1] != "t") and (len(path) < 3 or path[-3:] != "TTT"):
        new_cube = RubikCube(currCube.get_key())
        new_cube.move_top_right()
        yield (new_cube, path + "T")
    if (len(path) == 0 or path[-1] != "f") and (len(path) < 3 or path[-3:] != "FFF"):
        new_cube = RubikCube(currCube.get_key())
        new_cube.move_front_anti_clockwise()
        yield (new_cube, path + "F")


def solve(inputCube):
    """
    Solves the given Rubik's Cube using a breadth-first search.

    This function first checks if the cube is already solved or can be solved
    using the pre-calculated solutions. If not, it performs a breadth-first
    search to find the shortest solution path.

    Args:
        inputCube (RubikCube): The cube to solve.
    """
    solved, solvePath = checkSolved(inputCube)
    if solved:
        if solvePath == "":
            print("\nThe Cube is already solved. Nothing to do.\n")
        else:
            print("\nFound Solution: %s\n" % solvePath)
    else:
        cubeKeys = set([inputCube.get_key()])
        newcubes = [(inputCube, "")]
        solution_found = False
        try:
            while not solution_found:
                cubes, newcubes = newcubes, []
                for currCube, path in cubes:
                    for nextCube, operation in getAllMoves(currCube, path):
                        key = nextCube.get_key()
                        if key not in cubeKeys:
                            solved, solvePath = checkSolved(nextCube)
                            if solved:
                                print("\nFound Solution: %s%s\n" % (path + operation, solvePath))
                                solution_found = True
                                return

                            cubeKeys.add(key)
                            newcubes.append((nextCube, path + operation))
        except KeyboardInterrupt:
            pass


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
        cube = RubikCube(sys.argv[1])
        cube.print_cube()
        print("Solving...")
        t.join()
        solve(cube)
    else:
        cube = RubikCube("yyyyrrrrwwwwppppbbbbgggg")
        cube.print_cube()
        while True:
            cmdText = input("Please enter command: ")
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
                cube = RubikCube(cmdText[5:])
                cube.print_cube()
            elif cmdText == "exit":
                exit(0)
            elif cmdText != "" and set(cmdText).issubset(set("lLtTfFrRbBaA")):
                for cmdChar in cmdText:
                    if cmdChar == "l":
                        cube.move_left_down()
                    elif cmdChar == "t":
                        cube.move_top_left()
                    elif cmdChar == "f":
                        cube.move_front_clockwise()
                    elif cmdChar == "L":
                        cube.move_left_up()
                    elif cmdChar == "T":
                        cube.move_top_right()
                    elif cmdChar == "F":
                        cube.move_front_anti_clockwise()
                    elif cmdChar == "R":
                        cube.move_right_down()
                    elif cmdChar == "r":
                        cube.move_right_up()
                    elif cmdChar == "B":
                        cube.move_bottom_left()
                    elif cmdChar == "b":
                        cube.move_bottom_right()
                    elif cmdChar == "a":
                        cube.move_back_clockwise()
                    elif cmdChar == "A":
                        cube.move_back_anti_clockwise()

                cube.print_cube()
            else:
                print("Command not known. Possible commands are: solve, print, l, L, t, T, f, F, R, r, B, b, a, A, exit")

if __name__ == "__main__":
    main()
