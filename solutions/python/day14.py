import aoc
from collections import defaultdict
import math
"""
As I understand it, we need to traverse a linked list or other similar mapping to determine the amount of ORE required to produce 1 FUEL


The data structure is created when parsing the list of reactions.  They have the following form:

	N <NAME> [, N <NAME> ] => N <NAME>

	The mapping will look like:

	{
	NAME: {NAME2: N, NAME3: M}
	}

	Where NAME is created by N units of NAME2 and M units of NAME3


	Ultimately, I could recursively solve this by iterating down until I receive an ORE, returning the ultimate result
"""
DEBUG = False

def debug(msg):
	if DEBUG:
		print(msg)


class ReactionBook:

	def __init__(self, input_str):

		self._reactions = {}
		self.parse_reactions(input_str)

	def __getitem__(self, item):
		return self._reactions.__getitem__(item)

	def __setitem__(self, item, val):
		self._reactions.__setitem__(item, val)

	def __len__(self):
		return len(self._reactions)

	@classmethod
	def parse_reaction(cls, reaction_line):

		# Split by the reaction equality

		try:
			inputs_str, output_str = reaction_line.strip().split(' => ')
			output_qty, output_name = output_str.split(" ")
			output_qty = int(output_qty)
			inputs = {}
			for input_str in inputs_str.strip().split(','):

				input_qty, input_name = input_str.strip().split(' ')
				inputs[input_name] = int(input_qty) 

		except (TypeError, ValueError):
			print("Cannot parse line: ", reaction_line)
		else:

			return (output_name, output_qty), inputs

	def parse_reactions(self, input_str):

		for line in input_str.strip().split('\n'):
			(output_name, output_qty), inputs = self.parse_reaction(line)

			self._reactions[output_name] = {'in': inputs, 'qty': output_qty }

class Nanofactory:

	def __init__(self, reactions: ReactionBook):

		self.reactions = reactions
		self.store = defaultdict(int)  	# Store any remaining materials from production here
		self.ore_used = 0  				# Keep track of the ore used

	def take_from_store(self, name, qty):
		# Take what's needed from the store, return what is remaining

		if self.store[name] >= qty:
			debug(f"Taking {qty} {name} from store")
			self.store[name] -= qty
			return 0
		else:
			debug(f"Taking {self.store[name]} {name} from store")
			qty -= self.store[name]
			self.store[name] = 0
			return qty

	def produce(self, target_name: str, target_qty: int):

		"""
			Produce a target amount of an item.

			First check whether we can pull from the store, whats remaining needs to be produced

			Next determine how many batches of the target need to be made based off the reaction, 
				collect the inputs needed and their quantities
				calculate the remainder, this goes in the store

			Iteratively call produce on the required inputs
				If the reaction requires ORE, save this to the ore count, otherwise continue

			At the end, we should have the target item produced, the store filled with remainder amounts, and the amount of ore needed in production
			
		"""
		debug(f"Production Request: {target_qty} of {target_name}")

		need_to_produce = self.take_from_store(target_name, target_qty)

		if need_to_produce > 0:
			reaction_inputs = self.reactions[target_name]['in']
			reaction_qty = self.reactions[target_name]['qty']
			# how many batches are needed
			batch_qty = math.ceil(need_to_produce / reaction_qty)


			for reaction_input, input_qty in reaction_inputs.items():
				if reaction_input == 'ORE':
					ore_used = batch_qty * input_qty
					debug(f"Using {ore_used} ORE")
					self.ore_used += ore_used
					continue

				self.produce(reaction_input, batch_qty * input_qty)

			extra = batch_qty * reaction_qty - need_to_produce
			debug(f"Storing remaining {extra} of {target_name}  to store")
			self.store[target_name] += extra

	def how_much_fuel(self, ore_amount=1e12):
		# how much for one fuel

		fuel_produced = 1
		self.produce('FUEL', 1)
		single_fuel_needs = self.ore_used
		# Quick and dirty, how much

		# how much ore can we use
		while (ore_amount - self.ore_used) > single_fuel_needs:
			
			fuel_needed = math.floor((ore_amount - self.ore_used) / single_fuel_needs)
			fuel_produced += fuel_needed
			self.produce('FUEL', fuel_needed)

		return fuel_produced

def part1():

	with open('input/14.txt') as f:
		input_str = f.read().strip()

	reactions = ReactionBook(input_str)
	nanofactory = Nanofactory(reactions)

	nanofactory.produce('FUEL', 1)

	print(f"1 Fuel requires: {nanofactory.ore_used} ore")

	nanofactory = Nanofactory(reactions)
	fuel_amount = nanofactory.how_much_fuel()
	print(f"You can produce {fuel_amount} fuel")

def test1():
	input_str = '''\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
'''

	lines = input_str.strip().split('\n')

	expected_output = (('A', 10), {'ORE': 10})
	actual_output = ReactionBook.parse_reaction(lines[0]) 
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	expected_output = (('C', 1), {'A': 7, 'B': 1})
	actual_output = ReactionBook.parse_reaction(lines[2])
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	reactions = ReactionBook(input_str)
	assert len(reactions) == 6, len(reactions)


	factory = Nanofactory(reactions)
	factory.produce('FUEL', 1)

	expected_output = 31
	actual_output = factory.ore_used
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	print("Tests 1 passed")

# test1()

def test2():
	input_str = """\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""
	
	reactions = ReactionBook(input_str)
	factory = Nanofactory(reactions)

	factory.produce('FUEL', 1)
	expected_output = 13312
	actual_output = factory.ore_used
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	factory = Nanofactory(reactions)
	expected_output = 82892753
	actual_output = factory.how_much_fuel()
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"
	print("Tests 2 passed")

def test3():
	input_str = """\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""
	
	reactions = ReactionBook(input_str)
	factory = Nanofactory(reactions)

	factory.produce('FUEL', 1)
	expected_output = 180697 
	actual_output = factory.ore_used
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	factory = Nanofactory(reactions)
	expected_output = 5586022 
	actual_output = factory.how_much_fuel()
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	print("Tests 3 passed")

def test4():
	input_str = """\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""
	
	reactions = ReactionBook(input_str)
	factory = Nanofactory(reactions)

	factory.produce('FUEL', 1)
	expected_output = 2210736  
	actual_output = factory.ore_used
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	factory = Nanofactory(reactions)
	expected_output = 460664  
	actual_output = factory.how_much_fuel()
	assert actual_output == expected_output, f"Expected: {expected_output}. Got: {actual_output}"

	print("Tests 4 passed")

def run_tests():
	test1()
	test2()
	test3()
	test4()

# run_tests()

part1()  # 1037742


