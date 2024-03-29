#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Rubik Cube 2x2 Solver. 

Input format:
  Colors: 
    red = r
    white = w
    blue = b
    yellow = y
    purple = p
    green = g

Arguments:
      <Top><Front><Bottom><Back><Left><Right>
      tttt ffff   bbbb    aaaa  llll  rrrr
      e.G. rubik.py rgrggpyybbppwwbrwwgpyyrb
      or:  rubik.py rrwrbwwwpppyygyybrbbgggp  (cube in a cube -- very complex to solve)
    
    Order of surfaces on one side:
      -------
      |1. 2.|
      |3. 4.|
      -------

Available Commands in the Terminal:
  exit    exit the program
  print   print the current cube
  solve   try to find a solution for the current cube
  init    re-init the cube with a new side sequence
  random  randomize the current cube with 8 moves
  random4 randomize the current cube with 4 moves
  l/L     move LEFT down / LEFT up
  f/F     move FRONT clockwise / FRONT anticlockwise
  t/T     move TOP LEFT / TOP RIGHT
  
  The move-commands can be chained: e.G. lFtL
  
  http://www.mathematische-basteleien.de/miniwuerfel.htm
  http://www.jaapsch.net/puzzles/javascript/cube2j.htm  
  
  
  Very complex moves:
  ttlfTlFlFTLL cube in a cube
  lfllffTFttlt
  lftfLfLfftLT
  lltfLfLtFLTT
  
  TODO:
  * Move everything into a class for better reuse
  * document (doc-strings)
  * correct naming (make more intuitive)
  * Use Threads during solve
"""
import sys
import random
import threading

try:
    import readline
except ImportError:
    pass

# CONSTANTS ###################################################################
LEVEL_OF_PRECALCULATION = 4

R = "\x1b[1;31;41m R \x1b[0m"
W = "\x1b[1;37;47m W \x1b[0m"
B = "\x1b[1;34;44m B \x1b[0m"
Y = "\x1b[1;33;43m Y \x1b[0m"
P = "\x1b[1;35;45m P \x1b[0m"
G = "\x1b[1;32;42m G \x1b[0m"

TOP = 0
FRONT = 1
BOTTOM = 2
BACK = 3
LEFT = 4
RIGHT = 5
# CONSTANTS ###################################################################


# GLOBALS #####################################################################
preSolutionCubes = {}
# GLOBALS #####################################################################

def defaultCube(): 
    return [[[Y, Y], [Y, Y]],
            [[R, R], [R, R]],
            [[W, W], [W, W]],
            [[P, P], [P, P]],
            [[B, B], [B, B]],
            [[G, G], [G, G]]]

def copyCube(cube):
    return [[row[:] for row in side] for side in cube]

def printcube(cube):
    print "        ╔═══╤═══╗"
    print "        ║%s│%s║" % (cube[TOP][0][0], cube[TOP][0][1])
    print "        ╟───┼───╢"
    print "        ║%s│%s║" % (cube[TOP][1][0], cube[TOP][1][1])
    print "╔═══╤═══╬═══╪═══╬═══╤═══╦═══╤═══╗"
    print "║%s│%s║%s│%s║%s│%s║%s│%s║" % (cube[LEFT][0][0], cube[LEFT][0][1], cube[FRONT][0][0], cube[FRONT][0][1], cube[RIGHT][0][0], cube[RIGHT][0][1], cube[BACK][1][1], cube[BACK][1][0])
    print "╫───┼───╫───┼───╫───┼───╫───┼───╢"
    print "║%s│%s║%s│%s║%s│%s║%s│%s║" % (cube[LEFT][1][0], cube[LEFT][1][1], cube[FRONT][1][0], cube[FRONT][1][1], cube[RIGHT][1][0], cube[RIGHT][1][1], cube[BACK][0][1], cube[BACK][0][0])
    print "╚═══╧═══╬═══╪═══╬═══╧═══╩═══╧═══╝"
    print "        ║%s│%s║" % (cube[BOTTOM][0][0], cube[BOTTOM][0][1])
    print "        ╟───┼───╢"
    print "        ║%s│%s║" % (cube[BOTTOM][1][0], cube[BOTTOM][1][1])
    print "        ╚═══╧═══╝"
    
    
def calculateDefaultCubesOriented(cubes):
    c = defaultCube()
    ctb = topLeft(bottomLeft(copyCube(c)))
    ctbtb = topLeft(bottomLeft(copyCube(ctb)))
    ctbtbtb = topLeft(bottomLeft(copyCube(ctbtb)))
    
    cubes[get_key(c)] = (c, "")
    cubes[get_key(ctb)] = (ctb, "")
    cubes[get_key(ctbtb)] = (ctbtb, "")
    cubes[get_key(ctbtbtb)] = (ctbtbtb, "")

    for cube in [c, ctb, ctbtb, ctbtbtb]:
        for method1, method2 in [(rightDown, leftDown), (frontClockwise, backClockwise)]:
            nextCube = cube
            for _ in range(3):
                nextCube = method1(method2(copyCube(nextCube)))
                cubes[get_key(nextCube)] = (nextCube, "")


def checkSolved(testCube):
    key = get_key(testCube)
    if key in preSolutionCubes:
        path = preSolutionCubes[key][1]
        return (True, path.swapcase()[::-1])
    else:
        return (False, "")

def getAllMoves(currCube, path):
    if (len(path) == 0 or path[-1] != "L") and (len(path) < 3 or path[-3:] != "lll"):
        yield (leftDown(copyCube(currCube)), path + "l")
    if (len(path) == 0 or path[-1] != "T") and (len(path) < 3 or path[-3:] != "ttt"):
        yield (topLeft(copyCube(currCube)), path + "t")
    if (len(path) == 0 or path[-1] != "F") and (len(path) < 3 or path[-3:] != "fff"):
        yield (frontClockwise(copyCube(currCube)), path + "f")
    if (len(path) == 0 or path[-1] != "l") and (len(path) < 3 or path[-3:] != "LLL"):
        yield (leftUp(copyCube(currCube)), path + "L")
    if (len(path) == 0 or path[-1] != "t") and (len(path) < 3 or path[-3:] != "TTT"):
        yield (topRight(copyCube(currCube)), path + "T")
    if (len(path) == 0 or path[-1] != "f") and (len(path) < 3 or path[-3:] != "FFF"):
        yield (frontAntiClockwise(copyCube(currCube)), path + "F")
    
def leftDown(cube):
    (cube[TOP][0][0], cube[TOP][1][0],
    cube[FRONT][0][0], cube[FRONT][1][0],
    cube[BOTTOM][0][0], cube[BOTTOM][1][0],
    cube[BACK][0][0], cube[BACK][1][0],
    cube[LEFT][0][0], cube[LEFT][0][1],
    cube[LEFT][1][0], cube[LEFT][1][1]) = (cube[BACK][0][0], cube[BACK][1][0],
                                           cube[TOP][0][0], cube[TOP][1][0],
                                           cube[FRONT][0][0], cube[FRONT][1][0],
                                           cube[BOTTOM][0][0], cube[BOTTOM][1][0],
                                           cube[LEFT][1][0], cube[LEFT][0][0],
                                           cube[LEFT][1][1], cube[LEFT][0][1])
    return cube

def rightDown(cube):
    (cube[TOP][0][1], cube[TOP][1][1],
    cube[FRONT][0][1], cube[FRONT][1][1],
    cube[BOTTOM][0][1], cube[BOTTOM][1][1],
    cube[BACK][0][1], cube[BACK][1][1],
    cube[RIGHT][0][0], cube[RIGHT][0][1],
    cube[RIGHT][1][0], cube[RIGHT][1][1]) = (cube[BACK][0][1], cube[BACK][1][1],
                                           cube[TOP][0][1], cube[TOP][1][1],
                                           cube[FRONT][0][1], cube[FRONT][1][1],
                                           cube[BOTTOM][0][1], cube[BOTTOM][1][1],
                                           cube[RIGHT][0][1], cube[RIGHT][1][1],
                                           cube[RIGHT][0][0], cube[RIGHT][1][0])
    return cube

def rightUp(cube):
    rightDown(cube)
    rightDown(cube)
    rightDown(cube)
    return cube

def leftUp(cube):
    leftDown(cube)
    leftDown(cube)
    leftDown(cube)
    return cube

def topLeft(cube):
    (cube[FRONT][0][0], cube[FRONT][0][1],
    cube[LEFT][0][0], cube[LEFT][0][1],
    cube[BACK][1][0], cube[BACK][1][1],
    cube[RIGHT][0][0], cube[RIGHT][0][1],
    cube[TOP][0][0], cube[TOP][0][1],
    cube[TOP][1][0], cube[TOP][1][1]) = (cube[RIGHT][0][0], cube[RIGHT][0][1],
                                         cube[FRONT][0][0], cube[FRONT][0][1],
                                         cube[LEFT][0][1], cube[LEFT][0][0],
                                         cube[BACK][1][1], cube[BACK][1][0],
                                         cube[TOP][1][0], cube[TOP][0][0],
                                         cube[TOP][1][1], cube[TOP][0][1])
    return cube

def topRight(cube):
    topLeft(cube)
    topLeft(cube)
    topLeft(cube)
    return cube

def bottomLeft(cube):
    (cube[FRONT][1][0], cube[FRONT][1][1],
    cube[LEFT][1][0], cube[LEFT][1][1],
    cube[BACK][0][0], cube[BACK][0][1],
    cube[RIGHT][1][0], cube[RIGHT][1][1],
    cube[BOTTOM][0][0], cube[BOTTOM][0][1],
    cube[BOTTOM][1][0], cube[BOTTOM][1][1]) = (cube[RIGHT][1][0], cube[RIGHT][1][1],
                                         cube[FRONT][1][0], cube[FRONT][1][1],
                                         cube[LEFT][1][1], cube[LEFT][1][0],
                                         cube[BACK][0][1], cube[BACK][0][0],
                                         cube[BOTTOM][0][1], cube[BOTTOM][1][1],
                                         cube[BOTTOM][0][0], cube[BOTTOM][1][0])
    return cube

def bottomRight(cube):
    bottomLeft(cube)
    bottomLeft(cube)
    bottomLeft(cube)
    return cube

def frontClockwise(cube):
    (cube[TOP][1][0], cube[TOP][1][1],
    cube[LEFT][0][1], cube[LEFT][1][1],
    cube[BOTTOM][0][0], cube[BOTTOM][0][1],
    cube[RIGHT][0][0], cube[RIGHT][1][0],
    cube[FRONT][0][0], cube[FRONT][0][1],
    cube[FRONT][1][0], cube[FRONT][1][1]) = (cube[LEFT][1][1], cube[LEFT][0][1],
                                            cube[BOTTOM][0][0], cube[BOTTOM][0][1],
                                            cube[RIGHT][1][0], cube[RIGHT][0][0],
                                            cube[TOP][1][0], cube[TOP][1][1],
                                            cube[FRONT][1][0], cube[FRONT][0][0],
                                            cube[FRONT][1][1], cube[FRONT][0][1])
    return cube

def frontAntiClockwise(cube):
    frontClockwise(cube)
    frontClockwise(cube)
    frontClockwise(cube)
    return cube

def backClockwise(cube):
    (cube[TOP][0][0], cube[TOP][0][1],
    cube[LEFT][0][0], cube[LEFT][1][0],
    cube[BOTTOM][1][0], cube[BOTTOM][1][1],
    cube[RIGHT][0][1], cube[RIGHT][1][1],
    cube[BACK][0][0], cube[BACK][0][1],
    cube[BACK][1][0], cube[BACK][1][1]) = (cube[LEFT][1][0], cube[LEFT][0][0],
                                            cube[BOTTOM][1][0], cube[BOTTOM][1][1],
                                            cube[RIGHT][1][1], cube[RIGHT][0][1],
                                            cube[TOP][0][0], cube[TOP][0][1],
                                            cube[BACK][0][1], cube[BACK][1][1],
                                            cube[BACK][0][0], cube[BACK][1][0])
    return cube

def backAntiClockwise(cube):
    backClockwise(cube)
    backClockwise(cube)
    backClockwise(cube)
    return cube

def readCube(inputText):
    inputCube = defaultCube()
    charPosition = 0
    for side in (TOP, FRONT, BOTTOM, BACK, LEFT, RIGHT):
        for row in [0, 1]:
            for pos in [0, 1]:
                inputCube[side][row][pos] = eval(inputText[charPosition].upper())
                charPosition += 1
    return inputCube

def solve(inputCube):
    solved, solvePath = checkSolved(inputCube) 
    if solved:
        if solvePath == "":
            print "\nThe Cube is already solved. Nothing to do.\n" 
        else:
            print "\nFound Solution: %s\n" % solvePath
    else:
        cubeKeys = set([get_key(inputCube)])
        newcubes = [(inputCube, "")]
        solution_found = False
        try:
            while not solution_found:
                cubes, newcubes = newcubes, []
                # todo calculate in threads e.g. one thread for each cube, or 4 worker threads!
                # example: put the cubes in a queue and run 4 worker threads which empty the queue
                # introduce a global variable: solution_found to stop the worker threads.
                for currCube, path in cubes:
                    for nextCube, operation in getAllMoves(currCube, path):
                        key = get_key(nextCube)
                        if key not in cubeKeys:
                            solved, solvePath = checkSolved(nextCube)
                            if solved:
                                print "\nFound Solution: %s%s\n" % (operation, solvePath)
                                # todo: stop all thread if solution was found.
                                solution_found = True
                                return
                            
                            cubeKeys.add(key)
                            newcubes.append((nextCube, operation))
        except KeyboardInterrupt:
            pass
    
def random_moves(cube, count):
    cubeKeys = set([get_key(cube)])
    randomMoves = 0
    moves = [leftDown, leftUp, rightDown, rightUp,
             topLeft, topRight, bottomLeft, bottomRight,
             frontClockwise, frontAntiClockwise, backClockwise, backAntiClockwise]
    while randomMoves < count:
        move = random.choice(moves)
        move(cube)
        key = get_key(cube)
        if key not in cubeKeys:
            cubeKeys.add(key)
            randomMoves += 1

    return cube

def get_key(cube):
    return "".join([pos for side in cube for row in side for pos in row])

def preCalcCubes():
    # DefaultCubes: 24 Cubes
    # Level 1: 168 Cubes
    # Level 2: 816 Cubes
    # level 3: 3696 Cubes
    # Level 4: 16512 Cubes    
    calculateDefaultCubesOriented(preSolutionCubes)
    for _ in range(LEVEL_OF_PRECALCULATION):
        for key, (cube, path) in preSolutionCubes.items()[:]:
            for nextCube, nextPath in getAllMoves(cube, path):
                key = get_key(nextCube)
                if key not in preSolutionCubes:
                    preSolutionCubes[key] = (nextCube, nextPath)

def main():
    t = threading.Thread(target=preCalcCubes)
    t.start()
    
    print "-- Rubik 2x2 Solver --"

    if sys.argv[1:]:
        cube = readCube(sys.argv[1])
    else:
        cube = readCube("yyyyrrrrwwwwppppbbbbgggg")
    printcube(cube)
    while True:
        cmdText = raw_input("Please enter command: ")
        if cmdText == "solve":
            t.join()
            solve(cube)
        elif cmdText == "print":
            printcube(cube)
        elif cmdText == "random":
            random_moves(cube, 8)
            printcube(cube)
        elif cmdText == "random4":
            random_moves(cube, 4)
            printcube(cube)
        elif cmdText == "reset":
            cube = defaultCube()
            printcube(cube)
        elif cmdText[:5] == "init ":
            cube = readCube(cmdText[5:])
            printcube(cube)
        elif cmdText == "exit":
            exit(0)
        elif cmdText != "" and set(cmdText).issubset(set("lLtTfFrRbBaA")):
            for cmdChar in cmdText:
                if cmdChar == "l":
                    leftDown(cube)
                elif cmdChar == "t":
                    topLeft(cube)
                elif cmdChar == "f":
                    frontClockwise(cube)
                elif cmdChar == "L":
                    leftUp(cube)
                elif cmdChar == "T":
                    topRight(cube)
                elif cmdChar == "F":
                    frontAntiClockwise(cube)
                elif cmdChar == "R":
                    rightDown(cube)
                elif cmdChar == "R":
                    rightUp(cube)
                elif cmdChar == "B":
                    bottomLeft(cube)
                elif cmdChar == "B":
                    bottomRight(cube)
                elif cmdChar == "a":
                    backClockwise(cube)
                elif cmdChar == "A":
                    backAntiClockwise(cube)
                    
            printcube(cube)
        else:
            print "Command not known. Possible commands are: solve, print, l, L, t, T, f, F, R, R, B, B, a, A, exit"

if __name__ == "__main__":
    main()
