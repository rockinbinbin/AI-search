from sets import Set
from collections import deque
import heapq

# A class that wraps the heapq functionality
# into a convenient min heap container
# which always maintains the smallest element of
# a set of data, with O(log(n)) insertion and removal
# This heap does not support node cost updating, so just
# insert duplicate nodes with different path costs if necessary
class MinHeap:
	def __init__(self):
		self.container = []
	
	def push(self, obj):
		heapq.heappush(self.container, obj)

	# If obj is not in heap, push it into the heap
	# If obj is already in heap, but with a higher cost,
	# 	update the heap so that obj has the lower cost. Otherwise,
	# 	do nothing.
	def push_or_update(self, obj):
		if obj in self.container:
			index = self.container.index(obj)
			if obj.totalcost < self.container[index].totalcost:
				self.container[index] = self.container[-1]
				self.container.pop()
				heapq.heapify(self.container)
				heapq.heappush(self.container, obj)
		else:
			heapq.heappush(self.container, obj)

	def pop(self):
		return heapq.heappop(self.container)

	def top(self):
		return self.container[0]
	
	# So that you can call the python len() function on this object
	def __len__(self):
		return len(self.container)

# An implementation of the node class
# You may re-implement this if you wish
# But then be sure to re-implement the extract_path function
class node:
	node_count = 0
	def __init__(self, parent, position, pathcost=0, heuristic=0):
		self.idnum = node.node_count
		node.node_count += 1
		self.position = position
		self.pathcost = pathcost
		self.heuristic = heuristic
		self.totalcost = pathcost+heuristic
		self.parent = parent
		if parent is None:
			self.depth = 0
		else:
			self.depth = parent.depth+1

	# Less-than implemented so nodes can be put in MinHeap
	def __lt__(self, other):
		return self.totalcost < other.totalcost

	# Equality implemented so you can test whether nodes
	# are in a Set()
	# Nodes are equivalent if their positions are equal
	def __eq__(self, other):
		return (self.position == other.position)

	# Hash implemented so nodes can be put in Set()
	def __hash__(self):
		return hash(self.position)

# A dummy heuristic function that always returns 0
# Useful for searches that don't have a heuristic
def zero_heuristic(curpos, endpos):
	return 0

# Manhattan distance between curpos and endpos (tuples)
def manhattan(curpos, endpos):
	return abs(endpos[0]-curpos[0])+abs(endpos[1]-curpos[1])

# Euclidean distance between curpos and endpos (tuples)
def euclidean(curpos, endpos):
	return ((curpos[0]-endpos[0])**2+(curpos[1]-endpos[1])**2)**(0.5)

# A function that takes the current node, the grid,
# The goal position (endpos), and possibly the heuristic function, and returns a list of successors
def get_successors(curnode, grid, endpos, heuristic=zero_heuristic):
	# You may want to create several versions of this function

	successors = []

	if (curnode.position[0] < len(grid) and curnode.position[1] < len(grid[0])):
		#currnode exists

		if ((curnode.position[0] - 1) < len(grid) and (curnode.position[1]) < len(grid[0]) and (curnode.position[0] - 1) >= 0 and (curnode.position[1]) >= 0):
			#north exists
			if (grid[curnode.position[0] - 1][curnode.position[1]]): # not a wall
				i = curnode.position[0] - 1
				j = curnode.position[1]
				northPos = (i,j)
				northNode = node(curnode, northPos, 1 + heuristic(curnode.position, endpos))
				successors.append(northNode)

		if ((curnode.position[0]) < len(grid) and (curnode.position[1] + 1) < len(grid[0]) and (curnode.position[0]) >= 0 and (curnode.position[1] + 1) >= 0):
			#east exists
			if (grid[curnode.position[0]][curnode.position[1] + 1]): # not a wall
				i = curnode.position[0]
				j = curnode.position[1] + 1
				eastPos = (i,j)
				eastNode = node(curnode, eastPos, 2 + heuristic(curnode.position, endpos))
				successors.append(eastNode)

		if ((curnode.position[0] + 1) < len(grid) and (curnode.position[1]) < len(grid[0]) and (curnode.position[0] + 1) >= 0 and (curnode.position[1]) >= 0):
			#south exists
			if (grid[curnode.position[0] + 1][curnode.position[1]]): # not a wall
				i = curnode.position[0] + 1
				j = curnode.position[1]
				southPos = (i,j)
				southNode = node(curnode, southPos, 3 + heuristic(curnode.position, endpos))
				successors.append(southNode)

		if ((curnode.position[0]) < len(grid) and (curnode.position[1] - 1) < len(grid[0]) and (curnode.position[0]) >= 0 and (curnode.position[1] - 1) >= 0):
			#west exists
			if (grid[curnode.position[0]][curnode.position[1] - 1]): # not a wall
				i = curnode.position[0]
				j = curnode.position[1] - 1
				westPos = (i,j)
				westNode = node(curnode, westPos, 4 + heuristic(curnode.position, endpos))
				successors.append(westNode)

	return successors

# A function that tests whether a node is a goal node
def goal_test(curnode, endpos):
	return (curnode.position == endpos)

# extract_path takes a goal node and returns a path
# (a list of tuples) from the initial state to the goal.
# If you change the node class, re-implement this function
def extract_path(curnode):
	path = []
	while curnode is not None:
		path.append(curnode.position)
		curnode = curnode.parent
	return path[::-1]

# For all of the following search functions,
# "grid" is a python list of lists of integers describing the board
# Index the grid via grid[rowindex][columnindex]
# startpos is a tuple of the agent's starting position
# endpos is the location of the batter
# Do not change the arguments or return values of these functions
def depth_first_search(grid, startpos, endpos):
	# Perform depth-first search
	# Goal test at generation
	# Stack based search
	goalnode = node(None, endpos)
	total_nodes_generated = 0
	max_nodes_stored = 0
	num_iters = 0
	depth_of_goal = 0
	total_cost_of_goal = 0

	frontier = deque()
	startNode = node(None, startpos)
	frontier.append(startNode)
	exploredSet = Set()

	while (len(frontier) > 0):
		next_node = frontier.pop() # POP FROM SAME SIDE, TO IMMITATE STACK
		exploredSet.add(next_node)
		num_iters = num_iters + 1

		if (goal_test(next_node, endpos)):
			depth_of_goal = next_node.depth
			total_nodes_generated = next_node.node_count
			goalnode = next_node

			count = 0
			paths = extract_path(next_node)
			prevTuple = (0, 0) #safety initialization
			for nextTuple in paths:
				if (count < len(paths) and count > 0):
					if (prevTuple[0] < nextTuple[0]):
						#south
						total_cost_of_goal += 3
					elif (prevTuple[0] > nextTuple[0]):
						#north
						total_cost_of_goal += 1
					elif (prevTuple[1] < nextTuple[1]):
						#east
						total_cost_of_goal += 2
					else:
						#west
						total_cost_of_goal += 4
				prevTuple = nextTuple
				count = count + 1

			return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

		for unexploredNode in get_successors(next_node, grid, endpos):
			if ((unexploredNode not in exploredSet) and (unexploredNode not in frontier)):
				exploredSet.add(unexploredNode)
				frontier.append(unexploredNode)
				if (len(frontier) > max_nodes_stored):
					max_nodes_stored = len(frontier)

	return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

def iterative_deepening_search(grid, startpos, endpos):
	# Perform iterative deepening search
	# Goal test at generation
	goalnode = node(None, endpos)
	total_nodes_generated = 0
	max_nodes_stored = 0
	num_iters = 0
	depth_of_goal = 0
	total_cost_of_goal = 0
	d = 1

	frontier = deque()
	exploredSet = Set()
	while (d):
		startNode = node(None, startpos)
		frontier.append(startNode)
		print('outer loop called', d, len(frontier))
		while (len(frontier) > 0):
			print('inner loop called', d)
			next_node = frontier.pop() # POP FROM SAME SIDE, TO IMMITATE STACK
			exploredSet.add(next_node)
			num_iters = num_iters + 1

			if (goal_test(next_node, endpos)):
				depth_of_goal = next_node.depth
				total_nodes_generated = next_node.node_count
				goalnode = next_node
				count = 0
				paths = extract_path(next_node)
				prevTuple = (0, 0) #safety initialization
				for nextTuple in paths:
					if (count < len(paths) and count > 0):
						if (prevTuple[0] < nextTuple[0]):
							total_cost_of_goal += 3
						elif (prevTuple[0] > nextTuple[0]):
							total_cost_of_goal += 1
						elif (prevTuple[1] < nextTuple[1]):
							total_cost_of_goal += 2
						else:
							total_cost_of_goal += 4
					prevTuple = nextTuple
					count = count + 1
				return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

			for unexploredNode in get_successors(next_node, grid, endpos):
				if ((unexploredNode not in exploredSet) and (unexploredNode not in frontier) and (unexploredNode.depth <= d)):

					print(unexploredNode.position)

					exploredSet.add(unexploredNode)
					frontier.append(unexploredNode)
					if (len(frontier) > max_nodes_stored):
						max_nodes_stored = len(frontier)
				
				d = d + 1
		break
			#print(d)
			#d = d + 1
			#break			
	return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal


def breadth_first_search(grid, startpos, endpos):
	# Perform breadth-first search
	# Goal test at generation
	# Queue based search
	goalnode = node(None, endpos)
	total_nodes_generated = 0
	max_nodes_stored = 0
	num_iters = 0
	depth_of_goal = 0
	total_cost_of_goal = 0

	frontier = deque()
	startNode = node(None, startpos)
	frontier.append(startNode)
	exploredSet = Set()
	while (len(frontier) > 0):
		next_node = frontier.popleft() #POP FROM OPPOSITE SIDE TO IMMITATE QUEUE
		exploredSet.add(next_node)
		num_iters = num_iters + 1

		if (goal_test(next_node, endpos)):
			depth_of_goal = next_node.depth
			total_nodes_generated = next_node.node_count
			goalnode = next_node

			count = 0
			paths = extract_path(next_node)
			prevTuple = (0, 0) #safety initialization
			for nextTuple in paths:
				if (count < len(paths) and count > 0):
					if (prevTuple[0] < nextTuple[0]):
						#south
						total_cost_of_goal += 3
					elif (prevTuple[0] > nextTuple[0]):
						#north
						total_cost_of_goal += 1
					elif (prevTuple[1] < nextTuple[1]):
						#east
						total_cost_of_goal += 2
					else:
						#west
						total_cost_of_goal += 4
				prevTuple = nextTuple
				count = count + 1

			return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

		for unexploredNode in get_successors(next_node, grid, endpos):
			if ((unexploredNode not in exploredSet) and (unexploredNode not in frontier)):
				exploredSet.add(unexploredNode)
				frontier.append(unexploredNode)
				if (len(frontier) > max_nodes_stored):
					max_nodes_stored = len(frontier)

	return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

def uniform_cost_search(grid, startpos, endpos):
	# Perform uniform cost search
	# breadth first search, except with a MinHeap instead of deque.
	# Goal test at expansion
	goalnode = node(None, endpos)
	total_nodes_generated = 0
	max_nodes_stored = 0
	num_iters = 0
	depth_of_goal = 0
	total_cost_of_goal = 0

	frontier = MinHeap()
	startNode = node(None, startpos)
	frontier.push_or_update(startNode)
	exploredSet = Set()
	while (len(frontier) > 0):
		next_node = frontier.pop() #POP FROM OPPOSITE SIDE TO IMMITATE QUEUE
		exploredSet.add(next_node)
		num_iters = num_iters + 1

		if (goal_test(next_node, endpos)):
			depth_of_goal = next_node.depth
			total_nodes_generated = next_node.node_count
			goalnode = next_node

			count = 0
			paths = extract_path(next_node)
			prevTuple = (0, 0) #safety initialization
			for nextTuple in paths:
				if (count < len(paths) and count > 0):
					if (prevTuple[0] < nextTuple[0]):
						#south
						total_cost_of_goal += 3
					elif (prevTuple[0] > nextTuple[0]):
						#north
						total_cost_of_goal += 1
					elif (prevTuple[1] < nextTuple[1]):
						#east
						total_cost_of_goal += 2
					else:
						#west
						total_cost_of_goal += 4
				prevTuple = nextTuple
				count = count + 1

			return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

		for unexploredNode in get_successors(next_node, grid, endpos):
			if (unexploredNode not in exploredSet):
				exploredSet.add(unexploredNode)
				frontier.push_or_update(unexploredNode)
				if (len(frontier) > max_nodes_stored):
					max_nodes_stored = len(frontier)

	return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal
	
def a_star_search(grid, startpos, endpos, heuristic=manhattan):
	# Perform A* search
	# Goal test at expansion
	goalnode = node(None, endpos)
	total_nodes_generated = 0
	max_nodes_stored = 0
	num_iters = 0
	depth_of_goal = 0
	total_cost_of_goal = 0

	frontier = MinHeap()
	startNode = node(None, startpos)
	frontier.push_or_update(startNode)
	exploredSet = Set()
	while (len(frontier) > 0):
		next_node = frontier.pop() #POP FROM OPPOSITE SIDE TO IMMITATE QUEUE
		exploredSet.add(next_node)
		num_iters = num_iters + 1

		if (goal_test(next_node, endpos)):
			depth_of_goal = next_node.depth
			total_nodes_generated = next_node.node_count
			goalnode = next_node

			count = 0
			paths = extract_path(next_node)
			prevTuple = (0, 0) #safety initialization
			for nextTuple in paths:
				if (count < len(paths) and count > 0):
					if (prevTuple[0] < nextTuple[0]):
						#south
						total_cost_of_goal += 3
					elif (prevTuple[0] > nextTuple[0]):
						#north
						total_cost_of_goal += 1
					elif (prevTuple[1] < nextTuple[1]):
						#east
						total_cost_of_goal += 2
					else:
						#west
						total_cost_of_goal += 4
				prevTuple = nextTuple
				count = count + 1

			return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal

		for unexploredNode in get_successors(next_node, grid, endpos, heuristic):
			if (unexploredNode not in exploredSet):
				exploredSet.add(unexploredNode)
				frontier.push_or_update(unexploredNode)
				if (len(frontier) > max_nodes_stored):
					max_nodes_stored = len(frontier)

	return goalnode, total_nodes_generated, max_nodes_stored, num_iters, depth_of_goal, total_cost_of_goal


