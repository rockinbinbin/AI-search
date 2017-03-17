import sys
import copy
import importlib

def read_grid(filepointer):
	startpos = (0,0)
	endpos = (0,0)
	start = False
	end = False
	grid = [[int(e) for e in line.split()] for line in filepointer]
	height = len(grid)
	assert(height > 0)
	width = len(grid[0])
	assert(width > 0)
	for i,row in enumerate(grid):
		assert(len(row) == width)
		for j,e in enumerate(row):
			if e==2:
				startpos = (i,j)
				start = True
			if e==3:
				endpos = (i,j)
				end = True

	assert(start and end)
			
	return grid, startpos, endpos

def print_grid(grid):
	gridstr = ''
	for row in grid:
		for e in row:
			gridstr += str(e)+' '
		gridstr += '\n'
	print gridstr


class search_agent:
	def __init__(self, searchfunc, extract_path, heuristic=None):
		self.searchfunc = searchfunc
		self.heuristic = heuristic
		self.extract_path = extract_path

	def find_path(self, grid, startpos, endpos):
		goalnode = None
		maxnodes = 0
		iters = 0
		depth = 0
		totalcost = 0
		totalnodes = 0
		if self.heuristic is not None:
			goalnode, totalnodes, maxnodes, iters, depth, totalcost = self.searchfunc(grid, startpos, endpos, self.heuristic)
		else:
			goalnode, totalnodes, maxnodes, iters, depth, totalcost = self.searchfunc(grid, startpos, endpos)
		path = self.extract_path(goalnode)

		print 'Total nodes generated', totalnodes
		print 'Max nodes stored at once', maxnodes
		print 'Number of iterations', iters
		print 'Depth of goal', depth
		print 'Cost of path', totalcost
		print 'Length of path', len(path)
		return path


def run_simulation(searchgrid, startpos, endpos, module, searchtype, heuristic = None):
	agent = None
	if searchtype == 'dfs':
		agent = search_agent(module.depth_first_search, module.extract_path)
	elif searchtype == 'bfs':
		agent = search_agent(module.breadth_first_search, module.extract_path)
	elif searchtype == 'ucs':
		agent = search_agent(module.uniform_cost_search, module.extract_path)
	elif searchtype == 'astar':
		heuristicfunc = None
		if heuristic == 'manhattan':
			heuristicfunc = module.manhattan
		elif heuristic == 'euclidean':
			heuristicfunc = module.euclidean
		else:
			print "Unknown heuristic"
			assert(False)
		agent = search_agent(module.a_star_search, module.extract_path, heuristicfunc)
	elif searchtype == 'ids':
		agent = search_agent(module.iterative_deepening_search, module.extract_path)
	else:
		print "Invalid search type"
		assert(False)

	path = agent.find_path(searchgrid, startpos, endpos)

	outgrid = copy.deepcopy(searchgrid)
	pathlen = len(path)
	for j, t in enumerate(path):
		if j<(pathlen-1):
			nexttuple = path[j+1]
			if nexttuple[0]<t[0]:
				outgrid[t[0]][t[1]] = '^'
			elif nexttuple[0]>t[0]:
				outgrid[t[0]][t[1]] = '!'
			elif nexttuple[1]<t[1]:
				outgrid[t[0]][t[1]] = '<'
			elif nexttuple[1]>t[1]:
				outgrid[t[0]][t[1]] = '>'
		else:
			outgrid[t[0]][t[1]] = '*'

	print_grid(outgrid)


# python simulator.py searchmodule gridfile searchtype [heuristic]
if __name__ == '__main__':
	assert(len(sys.argv) > 3)
	module = importlib.import_module(sys.argv[1])
	filename = sys.argv[2]
	searchtype = sys.argv[3]
	heuristic = None
	if searchtype == 'astar':
		assert(len(sys.argv) > 4)
		heuristic = sys.argv[4]
		
	searchgrid, startpos, endpos = read_grid(open(filename, 'r'))			
	print_grid(searchgrid)
	run_simulation(searchgrid, startpos, endpos, module, searchtype, heuristic)

