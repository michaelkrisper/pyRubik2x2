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
    side ordering:
      TopFrontBottomBackLeftRight
    order of surfaces on one side:
      1. 2.
      3. 4.
    
    e.g. rgrggpyybbppwwbrwwgpyyrb

Available Commands in the Terminal:
  exit    exit the program
  print   print the current cube
  solve   try to find a solution for the current cube
  random  randomize the current cube
  l/L     move left down / left up
  f/F     move front clockwise / front anticlockwise
  t/T     move top left / top right
  
  The move-commands can be chained: e.g. lFtL
  
"""
import sys
import random

import readline

# backward compatibility for python 2 and python 3
try:
    input = raw_input
except NameError:
    pass

r = "\x1b[1;31;41m R \x1b[0m"
w = "\x1b[1;37;47m W \x1b[0m"
b = "\x1b[1;34;44m B \x1b[0m"
y = "\x1b[1;33;43m Y \x1b[0m"
p = "\x1b[1;35;45m P \x1b[0m"
g = "\x1b[1;32;42m G \x1b[0m"

top = 0
front = 1
bottom = 2
back = 3
left = 4
right = 5

def copyCube(cube):
    return [[row[:] for row in side] for side in cube]

def printcube(cube):
    print "        ╔═══╤═══╗"
    print "        ║%s│%s║" % (cube[top][0][0], cube[top][0][1])
    print "        ╟───┼───╢"
    print "        ║%s│%s║" % (cube[top][1][0], cube[top][1][1])
    print "╔═══╤═══╬═══╪═══╬═══╤═══╦═══╤═══╗"
    print "║%s│%s║%s│%s║%s│%s║%s│%s║" % (cube[left][0][0], cube[left][0][1], cube[front][0][0], cube[front][0][1], cube[right][0][0], cube[right][0][1], cube[back][1][1], cube[back][1][0])
    print "╫───┼───╫───┼───╫───┼───╫───┼───╢"
    print "║%s│%s║%s│%s║%s│%s║%s│%s║" % (cube[left][1][0], cube[left][1][1], cube[front][1][0], cube[front][1][1], cube[right][1][0], cube[right][1][1], cube[back][0][1], cube[back][0][0])
    print "╚═══╧═══╬═══╪═══╬═══╧═══╩═══╧═══╝"
    print "        ║%s│%s║" % (cube[bottom][0][0], cube[bottom][0][1])
    print "        ╟───┼───╢"
    print "        ║%s│%s║" % (cube[bottom][1][0], cube[bottom][1][1])
    print "        ╚═══╧═══╝"
    
def checkSolved(cube):
    for side in range(6):
        if not (cube[side][0][0] == cube[side][0][1] == cube[side][1][0] == cube[side][1][1]):
            return False
    return True
    
def leftDown(cube):
    (cube[top][0][0], cube[top][1][0],
    cube[front][0][0], cube[front][1][0],
    cube[bottom][0][0], cube[bottom][1][0],
    cube[back][0][0], cube[back][1][0],
    cube[left][0][0], cube[left][0][1],
    cube[left][1][0], cube[left][1][1]) = (cube[back][0][0], cube[back][1][0],
                                           cube[top][0][0], cube[top][1][0],
                                           cube[front][0][0], cube[front][1][0],
                                           cube[bottom][0][0], cube[bottom][1][0],
                                           cube[left][1][0], cube[left][0][0],
                                           cube[left][1][1], cube[left][0][1])
    return cube

def leftUp(cube):
    cube = leftDown(cube)
    cube = leftDown(cube)
    cube = leftDown(cube)
    return cube

def topLeft(cube):
    (cube[front][0][0], cube[front][0][1],
    cube[left][0][0], cube[left][0][1],
    cube[back][1][0], cube[back][1][1],
    cube[right][0][0], cube[right][0][1],
    cube[top][0][0], cube[top][0][1],
    cube[top][1][0], cube[top][1][1]) = (cube[right][0][0], cube[right][0][1],
                                         cube[front][0][0], cube[front][0][1],
                                         cube[left][0][1], cube[left][0][0],
                                         cube[back][1][1], cube[back][1][0],
                                         cube[top][1][0], cube[top][0][0],
                                         cube[top][1][1], cube[top][0][1])
    return cube

def topRight(cube):
    cube = topLeft(cube)
    cube = topLeft(cube)
    cube = topLeft(cube)
    return cube

def frontClockwise(cube):
    (cube[top][1][0], cube[top][1][1],
    cube[left][0][1], cube[left][1][1],
    cube[bottom][0][0], cube[bottom][0][1],
    cube[right][0][0], cube[right][1][0],
    cube[front][0][0], cube[front][0][1],
    cube[front][1][0], cube[front][1][1]) = (cube[left][1][1], cube[left][0][1],
                                            cube[bottom][0][0], cube[bottom][0][1],
                                            cube[right][1][0], cube[right][0][0],
                                            cube[top][1][0], cube[top][1][1],
                                            cube[front][1][0], cube[front][0][0],
                                            cube[front][1][1], cube[front][0][1])
    return cube

def frontAntiClockwise(cube):
    cube = frontClockwise(cube)
    cube = frontClockwise(cube)
    cube = frontClockwise(cube)
    return cube

def readCube():
    inputCube = defaultCube()
        
    if sys.argv[1:]:
        counter = 0
        inputText = sys.argv[1]
        for side in [top, front, bottom, back, left, right]:
            for row in [0, 1]:
                for pos in [0, 1]:
                    inputCube[side][row][pos] = eval(inputText[counter])
                    counter += 1
        
    return inputCube

def defaultCube():
    return [[[y, y], [y, y]],
            [[r, r], [r, r]],
            [[w, w], [w, w]],
            [[p, p], [p, p]],
            [[b, b], [b, b]],
            [[g, g], [g, g]]]

def main():
    cube = readCube()
    print "-- Rubik 2x2 Solver --"
    printcube(cube)
    while True:
        cmdText = input("Please enter command: ")
        if cmdText == "solve":
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
        elif cmdText == "exit":
            exit(0)
        elif cmdText != "" and set(cmdText).issubset(set("ltfLTF")):
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
            printcube(cube) 
        else:
            print "Command not known. Possible commands are: solve, print, l, t, f, L, T, F, exit"

def solve(inputCube):
    iteration = -1
    cubeKeys = set([get_key(inputCube)])
    solution_found = False
    newcubes = [(inputCube, "")] 
    while iteration < 9 and not solution_found:
        iteration += 1
        print "Cube count: %d, Iteration: %d" % (len(cubeKeys), iteration)
        cubes = newcubes
        newcubes = []
        for currCube, path in cubes:
            if checkSolved(currCube):
                print ""
                print "Found Solution: " + path
                print ""
                solution_found = True
                break
                
            moves = []
            if (len(path) == 0 or path[-1] != "L") and (len(path) < 3 or path[-3:] != "lll"): moves.append((leftDown(copyCube(currCube)), "l"))
            if (len(path) == 0 or path[-1] != "T") and (len(path) < 3 or path[-3:] != "ttt"): moves.append((topLeft(copyCube(currCube)), "t"))
            if (len(path) == 0 or path[-1] != "F") and (len(path) < 3 or path[-3:] != "fff"): moves.append((frontClockwise(copyCube(currCube)), "f"))
            if (len(path) == 0 or path[-1] != "l") and (len(path) < 3 or path[-3:] != "LLL"): moves.append((leftUp(copyCube(currCube)), "L"))
            if (len(path) == 0 or path[-1] != "t") and (len(path) < 3 or path[-3:] != "TTT"): moves.append((topRight(copyCube(currCube)), "T"))
            if (len(path) == 0 or path[-1] != "f") and (len(path) < 3 or path[-3:] != "FFF"): moves.append((frontAntiClockwise(copyCube(currCube)), "F"))
                
            for (nextCube, operation) in moves:
                key = get_key(nextCube)
                if key not in cubeKeys:
                    cubeKeys.add(key)
                    newcubes.append((nextCube, path + operation))
    
    if not solution_found:
        print "No solution found in %d iterations." % iteration

def random_moves(cube, count):
    cubeKeys = set([get_key(cube)])
    randomMoves = 0
    moves = [leftDown, topLeft, frontClockwise, leftUp, topRight, frontAntiClockwise]
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

if __name__ == "__main__":
    main()
