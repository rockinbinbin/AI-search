# Robin Mehta
# 8 Puzzle
import numpy
from numpy.random import randint

_goal_state = [[0,1,2],
               [3,4,5],
               [6,7,8]]

def main():
	puzzles = generatePuzzles()
	solvePuzzles(puzzles)


def generatePuzzles():
	puzzles = {}
	count = 0
	while (count <= 25000):
		value = numpy.random.randint(9, size=(3, 3))
		puzzles[count] = value
		count += 1
	return puzzles

def solvePuzzles(puzzles):
	


if __name__ == '__main__':
	main()