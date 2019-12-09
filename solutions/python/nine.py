from intcode import IntCodeComputer, DebugFlag

with open('input/nine.txt') as f:
	program = list(map(int, f.read().strip().split(',')))

computer = IntCodeComputer(program, debug=DebugFlag.OFF)
computer.run()
print(computer.output_value)

#  4261108180



