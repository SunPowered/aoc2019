import os
import collections

in_file = os.path.join(os.getcwd(), 'input', 'three.txt')
assert os.path.exists(in_file), "Missing input file: {}".format(in_file)

# The idea is to be able to traverse an (x,y) grid based off input instructions
#
# Instructions are of the form '<DIR><VAL>', such as 'R6' for RIGHT-6, 'D4' for 'DOWN-4'
#
# We require the manhattan distance (x + y) of the closest intersection
#
# This imposes us to keep track of the path (or points) traversed, and highlight any duplicates

Point = collections.namedtuple("Point", ("x", "y"))

def move_point(point: Point, direction: str, value: int):
	direction = direction.upper()

	if direction == 'R':
		return Point(point.x + value, point.y)

	elif direction == 'L':
		return Point(point.x - value, point.y)

	elif direction == 'U':
		return Point(point.x, point.y + value)

	elif direction == 'D':
		return Point(point.x, point.y - value)

	else:
		raise ValueError("Undefined direction: ", direction)


def update_history(hist: list, old_p: Point, new_p: Point):
	
	# Find all points between old and new points

	dx = new_p.x - old_p.x
	dy = new_p.y - old_p.y

	if dx == 0:
		# Vertical, apply over y
		if dy > 0:
			op = int.__add__
		else:
			op = int.__sub__
		intermediates = [Point(new_p.x, op(old_p.y, yi)) for yi in range(1, abs(dy)+1)]

	elif dy == 0:
		# Horizontal, apply over x
		if dx > 0:
			op = int.__add__
		else:
			op = int.__sub__
		intermediates = [Point(op(old_p.x ,xi), old_p.y) for xi in range(1, abs(dx)+1)]

	else:
		raise ValueError("Moving in more than one direction!", old_p, new_p)
	
	hist.extend(intermediates)

def run_wire(instructions: list):


	cur_p = Point(0, 0)  # Tuple to store the current location
	hist_p = []  # Initial history, this is a list of tuples
	hist_p.append(cur_p)

	#iterate through the instructions
	for instruction in instructions:
		
		# Split the direction and the value, force value to an int
		direction, value = instruction[0], int(instruction[1:])

		new_p = move_point(cur_p, direction, value)
		
		update_history(hist_p, cur_p, new_p)
	
		cur_p = new_p
	
	return hist_p

def run_program(instruction1: list, instruction2: list):
	matches = set.intersection(set(run_wire(instruction1)), set(run_wire(instruction2)))
	matches.remove(Point(0,0))

	return sorted([abs(p.x) + abs(p.y) for p in matches])[0]

# There are two sets of instructions for every game, we need to find the intersections between the two

def run_program_2(instruction1: list, instruction2: list):
	hist_1 = run_wire(instruction1)
	hist_2 = run_wire(instruction2)

	matches = set.intersection(set(hist_1), set(hist_2))
	matches.remove(Point(0,0))

	# Now need to calculate total number of steps to each of these match points
	return sorted(map(lambda x: hist_1.index(x) + hist_2.index(x), matches))[0]

def run_tests():

	# Test inputs
	test_instruction_1 = ["U7","R6","D4","L4"]
	test_hist_1 = run_wire(test_instruction_1)
	assert test_hist_1[-1] == Point(2, 3)

	ti2A = ["R8","U5","L5","D3"]
	ti2B = ["U7","R6","D4","L4"]

	assert run_program(ti2A, ti2B) == 6

	ti3A = ["R75","D30","R83","U83",'L12',"D49","R71","U7","L72"]
	ti3B = ["U62","R66","U55","R34","D71","R55","D58","R83"]

	assert run_program(ti3A, ti3B) == 159

	ti4A = ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
	ti4B = ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]

	assert run_program(ti4A, ti4B) == 135

	assert run_program_2(ti2A, ti2B) == 30
	assert run_program_2(ti3A, ti3B) == 610
	assert run_program_2(ti4A, ti4B) == 410

	print("Tests OK!")

# Run with file input
def run1():
	print()
	print("Part 1")
	with open(in_file) as f:
		in1, in2 = f.read().strip().split('\n')
		in1 = in1.split(',')
		in2 = in2.split(',')

	print(run_program(in1, in2))

# Run with file input
def run2():
	print()
	print("Part 2")
	with open(in_file) as f:
		in1, in2 = f.read().strip().split('\n')
		in1 = in1.split(',')
		in2 = in2.split(',')

	print(run_program_2(in1, in2))

# run_tests()
run1() # 260
run2() # 15612