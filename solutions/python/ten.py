from collections import defaultdict
from math import sqrt

'''
The Problem: 
	* Given a 2D ASCII map
	* Parse the grid locations of the asteriods.  
	* Next, find the best asteroid location that has the fewest blocked other asteroids, ie no clear line of sight.


The Solution:
	* Given a parsed map of points, we can find the set of unit vectors to all other points, then sort any multiple vector items to find the closest one
'''


class AsteroidMap:

	def __init__(self, map_str = None):

		self.map_str = map_str
		self.members = set([])
		self.width = 0
		self.height = 0

		if map_str is not None:
			self.parse_map()

	def parse_map(self, map_str=None):
		
		map_str = map_str or self.map_str

		width = map_str.index('\n')
		if map_str[width-1] == '\r':
			width -= 1

		for y, line in enumerate(map_str.split('\n')):
			if len(line) == 0:
				continue
			assert len(line) == width, "{} != {}".format(len(line), width)
			for x, pos in enumerate(line):
				if pos == '#':
					self.members.add((x, y))

		self.width = width
		self.height = y+1


	@property
	def size(self):
		return self.width, self.height

	def difference_vector(self, pointA: tuple, pointB: tuple):
		assert len(pointA) == len(pointB), "Bad input, require points of identical size"

		return tuple((pointB[i] - pointA[i] for i in range(len(pointA))))

	def unit_vector(self, vector: tuple)->float:
		x, y = vector
		norm = sqrt(self.vector_norm_sq(vector))
		return (round(x / norm,10), round(y/norm, 10))

	def vector_norm_sq(self, vector):
		x, y = vector
		return x**2 + y**2
	
	def all_unit_vectors(self, start_point: tuple):

		res = {}
		for point in self.members:
			if point == start_point:
				continue
			res[point]  = self.unit_vector(self.difference_vector(start_point, point))

		# Invert this for a useful lookup table
		inv = defaultdict(set)
		[inv[v].add(k) for k, v in res.items()]

		return res, inv

	def find_best_location(self):
		best_loc = None
		best_cnt = -1

		for p in self.members:
			cnt = len(self.detectable_asteroids(p))

			if cnt > best_cnt:
				best_cnt = cnt
				best_loc = p

		return best_loc, best_cnt

	def detectable_asteroids(self, point):

		# Find all the detectable asteroids from a point

		assert point in self.members, "No asteroid mapped to point: {}".format(point)

		def sorted_key(p):
			rel_p = (p[0] - point[0], p[1] - point[1])
			return self.vector_norm_sq((p[0] - point[0], p[1] - point[1]))
		
		uv_map, uv_map_inv = self.all_unit_vectors(point)

		detectable = {}
		for unit_vector, points in uv_map_inv.items():
			if len(points) == 1:
				detected_point = list(points)[0]
			else:
				detected_point = sorted(list(points), key=lambda p:  self.vector_norm_sq((p[0] - point[0], p[1] - point[1])) )[0]
			
			detectable[detected_point] = unit_vector
		return detectable

	def print_map(self, points=None, start_point=None, highlighted_points=None):

		points = points or self.members

		visual_map = ['.'*self.width for y in range(self.height)]

		print()
		for p in self.members:
			if p == start_point:
				ch = '*'
			elif highlighted_points is not None and p in highlighted_points:
				ch = '\u25A0'
			else:
				ch = '#'
			line = visual_map[p[1]]
			ch_idx = p[0]
			if ch_idx == 0:
				visual_map[p[1]] = ch + line[1:]
			else:
				visual_map[p[1]]= line[:ch_idx ] + ch + line[ch_idx+1:]

		for line in visual_map:
			print(line)

		print()

def part1():
	with open('input/ten.txt') as f:
		map_str = f.read().strip()

	asteroid_map = AsteroidMap(map_str)
	print("Best Location")
	best_loc, best_count = asteroid_map.find_best_location()
	print(best_loc, ": ", best_count)
	detected_asteroids = asteroid_map.detectable_asteroids(best_loc)
	asteroid_map.print_map(start_point=best_loc, highlighted_points=detected_asteroids)

def assert_best_location(map_str, expected_location, expected_count):
	data = AsteroidMap(map_str)

	best_loc, best_cnt = data.find_best_location()

	assert best_loc == expected_location, "Unexpected optimal location.  Expected: {}.  Got: {}".format(expected_location, best_loc)
	assert best_cnt == expected_count, "Unexpected optimal location count.  Expected: {}.  Got: {}".format(expected_count, best_cnt)

def tests1():

	test_map_1 = '''\
.#..#
.....
#####
....#
...##
'''

	data = AsteroidMap(test_map_1)

	assert (3,4) in data.members

	tests_map_2 = '''\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
'''
	assert_best_location(tests_map_2, (5, 8), 33)


	tests_map_3 = '''\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
'''
	assert_best_location(tests_map_3, (1, 2), 35)

	test_map_4 = '''\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
'''
	assert_best_location(test_map_4, (6, 3), 41)

	test_map_5 = '''\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
'''
	assert_best_location(test_map_5, (11, 13), 210)

	print("Tests 1 passed")


# tests1()
part1()  # (17, 22)  288