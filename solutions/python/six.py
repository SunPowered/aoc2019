import os
from collections import defaultdict
from itertools import chain

in_file = os.path.join(os.getcwd(), 'input', 'six.txt')

assert os.path.exists(in_file), "No file found: {}".format(in_file)

def parse_orbit(line):
	return line.strip().split(')')

def parse_orbits(in_f):
	orbits = defaultdict(set)
	with open(in_f) as f:
		for line in f:
			parent, child = parse_orbit(line)
			orbits[parent].add(child)
	return orbits

def parse_orbits_dir(in_f):
	orbits = {}
	with open(in_f) as f:
		for line in f:
			parent, child = parse_orbit(line)
			# Init parent and/or child
			if parent not in orbits:
				orbits[parent] = {'c': set(), 'p': None}
			if child not in orbits:
				orbits[child] = {'c': set(), 'p': parent}
			orbits[parent]['c'].add(child)
			orbits[child]['p'] = parent
	return orbits	

def iter_nodes(orbits, node, parent=None):
	# Produce an iterable of the orbits
	# This will be a recursive function
    #        G - H       J - K - L
    #       /           /
    #COM - B - C - D - E - F
    #               \
    #                I
	#
	# Starting: E
	# Returns: EF, EJ, EK, EL, JK, JL, KL

	# I need to write out this thought process, iterative functions hurt my brain
	# Start at node E, the parent.  All links will be preceded by the parent
	# Iterate over children, [F, J]
	# F is not a parent, yield EF
	# J is a parent, recurse passing E as the parent
	# J has child K, which is a parent to L, 
	# L is not a parent, yield EL
	# Exhausted children of K, yield EK.  Exhausted children of J, yield EJ
	# Now, begin again at J and repeat ... this is a little more confusing

	if node not in orbits:
		return
	parent = parent or node  # Top level when parent is the node, assume this is what is intended by not passing it

	for v in orbits[node]['c']:  # Iterate over children
		
		if v in orbits:
			# Parent node
			for p, child in iter_nodes(orbits, v, parent=parent):
				yield p, child

		yield parent, v

def iter_orbits(orbits):
	# Traverse the direct and indirect orbits
	# start_node = find_start_node(orbits)  # Easy way to find the main root
	
	# Iterate over all the nodes, find it's tree
	for p in orbits:
		for parent, child in iter_nodes(orbits, p):
			yield parent, child

def iter_parents(orbits, node):
	
	parent = orbits[node]['p']
	yield parent  
	if orbits[parent]['p'] is None:  # Reached the top level node
		return 
	for p in iter_parents(orbits, parent):
		yield p

def find_common_ancestor(orbits, nodeA, nodeB):

	ancA = list(iter_parents(orbits, nodeA))
	ancB = list(iter_parents(orbits, nodeB))

	common = None
	dist = 0
	for i, p in enumerate(ancA):
		if p in ancB:
			common = p
			dist += i
			dist += ancB.index(p) 
			break
	else:
		print("No common ancestor")


	return common, dist



def part1():
	print()
	print("Part 1")
	orbits = parse_orbits_dir('input/six.txt')
	print(len(list(iter_orbits(orbits))), " orbits")

def part2():
	#print(list(iter_parents(orbits, 'YOU')))
	#print(list(iter_parents(orbits, 'SAN')))
	orbits = parse_orbits_dir('input/six.txt')
	print(find_common_ancestor(orbits,  'YOU', 'SAN'))

part1()  # 162439
part2()  # ('HYC', 367)