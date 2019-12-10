from collections import defaultdict
import math

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
		self.destroyed_asteroids = list()
		self.width = 0
		self.height = 0

		if map_str is not None:
			self.parse_map()

	def parse_map(self, map_str=None):
		
		self.map_str = map_str or self.map_str

		width = self.map_str.index('\n')
		if self.map_str[width-1] == '\r':
			width -= 1

		for y, line in enumerate(self.map_str.split('\n')):
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
		norm = math.sqrt(self.vector_norm_sq(vector))
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

	def destroy_asteroid(self, point):
		if point not in self.members:
			raise ValueError("No asteroid found at point ", point)
		self.members.remove(point)
		self.destroyed_asteroids.append(point)

	def destroy(self, point):
		# begin with vector [0,-1], rotate clockwise 
		# x: 0 -> 1 -> 0 -> -1
		# y: -1 -> 0 -> 1 -> 0
		# maybe convert all unit vectors to degrees from up and sort?

		# Create a copy of the map
		destroyed_map = AsteroidMap(self.map_str)
		# destroyed_map.members.remove(point)
		# Get detectable asteroids
		cnt = 0 
		
		while len(destroyed_map.members) > 1:
			# import pdb; pdb.set_trace()
			detectable = destroyed_map.detectable_asteroids(point)
			detectable_inv = {v :k for k, v in detectable.items()}

			for uv in sorted(detectable_inv.keys(), key=lambda p: math.pi - math.atan2(*p)):
				cnt += 1

				destroyed_point = detectable_inv[uv]
				# Reverse lookup the point
				destroyed_map.destroy_asteroid(destroyed_point)
				
		return destroyed_map.destroyed_asteroids


def part1():
	with open('input/ten.txt') as f:
		map_str = f.read().strip()

	asteroid_map = AsteroidMap(map_str)
	print("Best Location")
	best_loc, best_count = asteroid_map.find_best_location()
	print(best_loc, ": ", best_count)
	detected_asteroids = asteroid_map.detectable_asteroids(best_loc)
	asteroid_map.print_map(start_point=best_loc, highlighted_points=detected_asteroids)
	return asteroid_map

def part2():
	with open('input/ten.txt') as f:
		map_str = f.read().strip()

	asteroid_map = AsteroidMap(map_str)

	# Find the best location
	best_loc, best_count = asteroid_map.find_best_location()

	print("Best location at: ", best_loc)
	destroyed_asteroids = asteroid_map.destroy(best_loc)

	d_ast_200 = destroyed_asteroids[199]
	print("200th asteroid destroyed is ", d_ast_200)
	print("p.x * 100 + p.y = ", d_ast_200[0]*100 + d_ast_200[1])

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

def tests2():
	test_map = '''\
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
	asteroid_map = AsteroidMap(test_map)

	best_loc, _ = asteroid_map.find_best_location()

	d_ast = asteroid_map.destroy(best_loc)

	assert d_ast[0] == (11, 12)
	assert d_ast[1] == (12, 1)
	assert d_ast[2] == (12, 2)
	assert d_ast[9] == (12, 8)
	assert d_ast[19] == (16, 0)
	assert d_ast[49] == (16, 9)
	assert d_ast[99] == (10, 16)
	assert d_ast[198] == (9, 6)
	assert d_ast[199] == (8, 2)
	assert d_ast[200] == (10, 9)
	assert d_ast[298] == (11, 1)
	print("Tests 2 passed")

# tests1()

# tests2()
part1()  # (17, 22)  288
part2()  # (6, 16) -> 616