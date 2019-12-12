import os
import math

in_file = os.path.join(os.getcwd(), 'input', '01.txt')

assert os.path.isfile(in_file)
assert os.path.exists(in_file)


def fuel_req(mass):
	return math.floor(mass / 3) - 2

assert fuel_req(12) == 2
assert fuel_req(14) == 2
assert fuel_req(1969) == 654
assert fuel_req(100756) == 33583

with open(in_file) as f:
	total_fuel = sum([fuel_req(int(line)) for line in f])

print("1. Total Fuel Required: ", total_fuel)


def recur_fuel_req(mass):

	f = fuel_req(mass)
	total = 0

	while f > 0:
		total += f
		f = fuel_req(f)

	return total

assert recur_fuel_req(14) == 2
assert recur_fuel_req(1969) == 966
assert recur_fuel_req(100756) == 50346

with open(in_file) as f:
	total_fuel = sum([recur_fuel_req(int(line)) for line in f])

print("2. Total Fuel Required: ", total_fuel)

# 1. 3299598
# 2. 4946546