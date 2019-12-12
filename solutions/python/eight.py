import os
from typing import List
in_file = os.path.join(os.getcwd(), 'input', '08.txt')


def parse_layers(data: List[int], width: int, height: int):

	layers = []
	idx = 0
	
	# We should have layers (w x h) in size
	assert len(data) % width * height == 0

	
	while idx < len(data):
		
		layer = []
		for h in range(height):
			layer.append(data[idx:idx+width])
			idx += width
		layers.append(layer)

	return layers

def count_values(layer: list, val: int):
	return sum(map(lambda i: i == val, [y for x in layer for y in x]))

def get_pixel(layers, coords):
	# First get the slice of layers for this pixel

	layer_vals = [layer[coords[0]][coords[1]] for layer in layers]

	# Essentially the first value that is not a 2
	for v in layer_vals:
		if v != 2:
			return v
	return 2

def render_row(row):
	# 0 is black, 1 is white, 2 is transparent
	rendered = []
	for r in row:
		if r == 0:
			rendered.append(' ')
		elif r == 1:
			rendered.append("\u25A0")
		elif r == 2:
			rendered.append(' ')
	print("".join(rendered))

def test_parsing():

	layers = parse_layers([1,2,3,4,5,6,7,8,9,0,1,2], 3, 2)
	assert len(layers) == 2
	assert layers[1][0] == [7,8,9]
	print("Parser tests passed!")

def test_layer_collecting():

	layers = parse_layers([0,2,2,2,1,1,2,2,2,2,1,2,0,0,0,0], 2, 2)

	assert get_pixel(layers, (0,0)) == 0
	assert get_pixel(layers, (0,1)) == 1
	assert get_pixel(layers, (1,0)) == 1
	assert get_pixel(layers, (1,1)) == 0

	print("Layer collection tests passed")

# test_layer_collecting()

def part1():
	print("Part 1")
	with open(in_file) as f:
		data = list(map(int, f.read().strip()))

	layers = parse_layers(data, 25, 6)

	# Find the layer with the fewest 0 digits
	validation_layer_idx = sorted([(i, count_values(layer, 0)) for i, layer in enumerate(layers)], key=lambda tup: tup[1])[0][0]
	validation_layer = layers[validation_layer_idx]

	# Result is # of 1's in the validation layer multiplied by the number of 2's
	print(count_values(validation_layer, 1) * count_values(validation_layer, 2))
	print()

def part2():
	print("Part 2")
	with open(in_file) as f:
		data = list(map(int, f.read().strip()))

	layers = parse_layers(data, 25, 6)

	final_image = []

	for row in range(6):
		final_image.append([get_pixel(layers, (row, col)) for col in range(25)])

	print("Rendering Image")
	print()
	for row in final_image:
		render_row(row)

part1()  # 1620
part2()  # BCYEF
