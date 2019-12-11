from enum import Enum
from intcode import IntCodeComputer, StatusFlag
from collections import defaultdict

class RobotDirection(Enum):

	UP = '^'
	DOWN = 'v'
	LEFT = '<'
	RIGHT = '>'


class HullPaintingRobot:

	def __init__(self, program=None):


		self.current_loc = (0, 0)  						# The current location of the robot
		self.current_direction = RobotDirection.UP  	# This current direction robot is facing
		self.state =  defaultdict(bool) 				# Dict of painted indices and current color.  [0:black, 1: white] Default is black 
		self.computer = IntCodeComputer(program, input_user=self.iter_current(), pause_on_output=True)

		# This is the map of directions to move to when provided the direction input  ie. new_direction = self.direction_map[self.current_direction][turn_cmd]
		self.direction_map = {
			RobotDirection.UP: 		[RobotDirection.LEFT, 	RobotDirection.RIGHT],
			RobotDirection.DOWN: 	[RobotDirection.RIGHT, 	RobotDirection.LEFT],
			RobotDirection.LEFT: 	[RobotDirection.DOWN, 	RobotDirection.UP],
			RobotDirection.RIGHT: 	[RobotDirection.UP, 	RobotDirection.DOWN]
		}

	def move(self, direction: int):
		self.current_direction = self.direction_map[self.current_direction][direction]

		if self.current_direction == RobotDirection.UP:
			self.current_loc = (self.current_loc[0], self.current_loc[1]+1)
		elif self.current_direction == RobotDirection.DOWN:
			self.current_loc = (self.current_loc[0], self.current_loc[1]-1)
		elif self.current_direction == RobotDirection.LEFT:
			self.current_loc = (self.current_loc[0]-1, self.current_loc[1])
		elif self.current_direction == RobotDirection.RIGHT:
			self.current_loc = (self.current_loc[0]+1, self.current_loc[1])
		
	def find_bounds(self, min_size=3):

		# Find the most extreme x and y values
		x_bounds = [ -1 * min_size, min_size ]
		y_bounds = [ -1 * min_size, min_size ]

		for x, y in self.state:
			if x > x_bounds[1]:
				x_bounds[1] = x
			elif x < x_bounds[0]:
				x_bounds[0] = x

			if y > y_bounds[1]:
				y_bounds[1] = y
			elif y < y_bounds[0]:
				y_bounds[0] = y
		return x_bounds, y_bounds

	def print_state(self, bounds=None, size=None):
		# Initialize the empty map  
		size = size or 6

		x_bounds, y_bounds = self.find_bounds(min_size=6)
		print_state = [['.' for i in range(x_bounds[0], x_bounds[1]+1)] for i in range(y_bounds[0], y_bounds[1]+1)]

		# Change all white painted squares
		for x, y in self.state:
			if self.state[(x,y)]:
				print_state[y-y_bounds[0]][x-x_bounds[0]] = '#' 

		# Print your current position and 
		print_state[self.current_loc[1]-y_bounds[0]][self.current_loc[0]-x_bounds[0]] = self.current_direction.value

		print()
		for row in print_state[::-1]:
			print("".join(row))


	def iter_current(self):

		# This should output an iterable compatible with the intcode computer input_vals param

		while True:
			# Output the color of the current position
			yield int(self.state[self.current_loc])

	def paint_current_location(self, paint_color):
		self.state[self.current_loc] = bool(paint_color)

	def run(self):

		# The robot interacts with the computer
		# The robot will input any 

		assert self.computer.status == StatusFlag.READY, "Intcode computer is not ready to run"
		counter = 0
		while self.computer.status != StatusFlag.FINISHED:
			counter += 1
			# print("DEBUG: |{}| Current Location: {}.  Current State: {}".format(counter, self.current_loc, int(self.state[self.current_loc])))
			# Get two output values at a time
			
			self.computer.run()
			if self.computer.status == StatusFlag.FINISHED:
				break
			self.computer.run()
			
			paint_color, new_direction = self.computer.output_value
			self.computer.output_value = None

			# print("DEBUG: Output Received {} {}".format(do_paint, new_direction))

			
			self.paint_current_location(paint_color)

			self.move(new_direction)		

		print("Done")

def read_program():
	with open('input/11.txt') as f:
		program = list(map(int, f.read().strip().split(',')))
	return program

def part1():
	print("Part 1")
	program = read_program()
	robot = HullPaintingRobot(program)
	print("Running")
	robot.run()
	print(len(robot.state))
	robot.print_state()
	print("Finished")

def part2():
	print("Part 2")
	program = read_program()
	robot = HullPaintingRobot(program)
	robot.state[robot.current_loc] = True   # Set the current location white
	print("Running")
	robot.run()
	robot.print_state()
	print("Finished")

# part1() # 1885
part2()  # BFEAGHAF

# robot = HullPaintingRobot()
