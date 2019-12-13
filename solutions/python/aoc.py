import time

def read_input(filename):
	with open(f'input/{filename}') as f:
		content = f.readlines()

	return [line.strip() for line in content]

def read_program(filename):
	with open(f'input/{filename}') as f:
		program = list(map(int, f.read().strip().split(',')))
	return program

def timer(func):
	def wrapper(*args, **kwargs):
		start_time = time.time()
		res = func(*args, **kwargs)
		print(f"\nTime required: {(time.time() - start_time)*1000:.2f} ms\n")
		return res
	return wrapper