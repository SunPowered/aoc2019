import os
import numpy as np

in_file = os.path.join(os.getcwd(), 'input', 'two.txt')
assert os.path.isfile(in_file)
assert os.path.exists(in_file)


# We read the input file and parse into 4 int tuples
# (OP_CODE, PARAM1, PARAM2, OUTPUT)
# OP_CODE := {1, 2, 99}
# 1 :=> PARAM1 + PARAM2 -> *OUTPUT
# 2 :=> PARAM1 * PARAM2 -> *OUTPUT
# 99 :=> <STOP>

DEBUG = False

def debug(msg):
	if DEBUG:
		print(msg)

def run_program(mem: np.ndarray):
	
	# Iterate one location at a time, curr_loc is current location
	# If OP_CODE is 1 or 2, read the next 3 digits and process
	# If OP_CODE is 99, stop the program and return the current memory state

	# Assert memory is sane
	assert mem.ndim == 1, "Memory must be a linear block"
	assert mem.dtype == np.int32, "Wrong memory format, I need int32"
	
	curr_loc = 0
	while curr_loc < len(mem):
		opcode = mem[curr_loc]
		debug("Found opcode {} at loc {}".format(opcode, curr_loc))

		if opcode == 99:
			debug("program exit code caught, bye bye")
			break

		elif opcode == 1:
			p1, p2, op = mem[curr_loc+1:curr_loc+4] 
			curr_loc += 4
			debug("Params: {}".format((p1, p2, op)))
			mem[op] = mem[p1] + mem[p2]

		elif opcode == 2:
			p1, p2, op = mem[curr_loc+1:curr_loc+4] 
			curr_loc += 4
			debug("Params: {}".format((p1, p2, op)))
			mem[op] = mem[p1] * mem[p2]
		else:
			raise ValueError("Caught bad opcode: ", opcode, " at location: ", cur_loc, ". I don't know what to do!")

		debug(mem)
	return mem


def make_array(lst):
	return np.array(lst, dtype=int)

with open(in_file) as f:
	data = make_array(list(map(int, f.read().split(','))))

def try_noun_verb(mem: np.ndarray, noun: int, verb: int):
	# Manual state assignment from problem
	mem[1] = noun
	mem[2] = verb

	mem = run_program(mem)

	return mem[0] == 19690720

# Brute force, noun := {0, 99} | verb := {0, 99}

def iter_nv():
	for n in range(0, 99):
		for v in range(0, 99):
			mem = data.copy()
			if try_noun_verb(mem, n, v):
				return n, v
	return None, None    # No values worked


n, v = iter_nv()

if n is None or v is None:
	print("No good values found!")
else:
	print("Noun: ", n, ". Verb: ", v)
	print("Output: ", 100 * n + v)
