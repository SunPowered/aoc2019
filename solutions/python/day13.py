import aoc
import intcode
import enum

class TileID(enum.IntEnum):

	EMPTY = 0
	WALL = 1
	BLOCK = 2
	PADDLE = 3
	BALL = 4

@aoc.timer
def solve():

	# Setup computer
	print("Solving Day 13")
	program = list(map(int, aoc.read_program('13.txt')))
	computer = intcode.IntCodeComputer(program, pause_on_output=True)

	state = {}

	while computer.status != intcode.StatusFlag.FINISHED:

		# parse 3 output values
		for i in range(3):
			try:
				computer.run()
			except intcode.ProgramFinished:
				print("Program end found")
				break
		
		if computer.status != intcode.StatusFlag.FINISHED:
			x, y, t_id = computer.output_value
			computer.output_value = None

			state[(x, y)] = t_id

	total_block_tiles = sum([t_id == TileID.BLOCK.value for t_id in state.values()])
	print(f"Total Blocks: {total_block_tiles}")


solve()