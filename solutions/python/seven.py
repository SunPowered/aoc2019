from intcode import IntCodeComputer, StatusFlag, DebugFlag
from itertools import permutations
#
# A series of amplifiers needs to be configured.
#   USing the puzzle input as a InCode program, we 
#   need to find the amplifier settings that produces the highest output

#  The program is run on each amplifier, sequentially  
#  First it will ask for the phase setting of the amplifier, followed by the input value
#  This means the computer needs to be able to accept more than one input value when automated.

#  There are 5 amplifiers, and they will each have an int setting between 0 and 4 with *no repeats*
#  We need to brute force all settings permutations, run each through the program, record the output and input if it is a max.


def part1():
	print()
	print("Part 1")

	with open('input/seven.txt') as f:
		program = list(map(int, f.read().strip().split(',')))
	computer = IntCodeComputer(program, debug=DebugFlag.OFF)
	
	mo = -1
	mv = None

	for phases in permutations(range(5)):

		last_input = 0
		for phase in phases:
			computer.run(input_vals=(phase, last_input))
			last_input = computer.output_value

		if last_input > mo:
			mo = last_input
			mv = phases

	print(mo, mv)

def part2():

	# This time a feedback loop, where the output of the last result is fed into the initial and repeated
	# Phase settings are between 5 and 9, no repeats.
	# We must initialize and maintain state of all the computers
	print()
	print("Part 2")
	
	with open('input/seven.txt') as f:
		program = list(map(int, f.read().strip().split(',')))

	max_val = -1
	max_phase = None
	
	for phases in permutations(range(5, 10)):

		# Intiialize computers
		computers = [IntCodeComputer(program, input_user = p, pause_on_output=True) for p in phases]
		for computer in computers:
			computer.run()

		last_output = 0
		computers[0].run()

		while not all([ c.status == StatusFlag.FINISHED for c in computers]):
			for computer in computers:
				if computer.status != StatusFlag.FINISHED:
					computer.run(input_vals=last_output)
					last_output = computer.output_value
			# print([(c.output_value, c.status) for c in computers])

		result = last_output
		if result > max_val:
			max_val = result
			max_phase = phases

	print(max_val, max_phase)

part1()  # 118936 (2, 1, 4, 3, 0)
part2()  # 57660948 (9, 7, 6, 5, 8)


