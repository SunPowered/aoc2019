from intcode import IntCodeComputer, DebugFlag

with open('input/09.txt') as f:
	program = list(map(int, f.read().strip().split(',')))

computer = IntCodeComputer(program, debug=DebugFlag.OFF)
computer.run()
print(computer.output_value)

# 1 -> 4261108180
# 2 -> 77944


