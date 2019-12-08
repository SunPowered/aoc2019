#
# Password:
#
# 6 digit
# Value within range of puzzle input
# Two adjacent digits are the same
# Going left to right, the digits only increase, never decrease

password_range = (134792, 675810)

#
# I could brute force it, check each one digit by digit
#
# I could also come up with a way to skip to the next valid password, iterate over these valid passwords and count the iterations

# Attempting the second way, 
# - First check is whether the digits are all increasing
# - If no, then starting from the left, find the first instance of a decreasing digit, 
#		replace the remaining ones with the digit prior.  ie.  1356378 -> 1356666.  This ensures a repeat condition is also met
# - If yes, then check whether any repeating.  


# 1346789 -> 1346799
# 1111122 -> 1111113
# 1111119 -> 1111122

def check_number(n: int):
	# Split up into an iterable of ints
	it = map(int, str(n))

	is_duplicate = None

	duplicates = []
	tmp_dup = None  # None, or ('value', count )
	prev = next(it)  # Store first element
	
	for i, curr in enumerate(it):

		if curr < prev:
			return False, duplicates  # Decreasing digits, return out
		
		elif curr == prev:  # Repeating char found
			# Check whether next character is the same, if so, not a dup 
			# Are we already in a duplicate grouping?
			if tmp_dup is not None:
				# Already in a duplicate group, add to the count
				tmp_dup = (curr, tmp_dup[1] + 1)
			else:
				# New group
				tmp_dup = (curr, 2)
		
		else:
			if tmp_dup is not None:
				# End of repeating group
				duplicates.append(tmp_dup)
				tmp_dup = None
		
		prev = curr

	# Catch duplicates at the end
	if tmp_dup is not None:
		duplicates.append(tmp_dup)

	return True, duplicates

def check_duplicates(duplicates: list):
	# Check that one of the elements has a count of 2

	for duplicate in duplicates:
		if duplicate[1] == 2:
			return True
	return False

def brute_force(min_r: int, max_r: int):

	cnt = 0
	for v in range(min_r, max_r + 1):
		is_inc, duplicates = check_number(v)

		# Ensure there is a 2-count duplicate

		if is_inc and duplicates:
			cnt += 1

	print("Counted {} valid passwords in range {}:{}".format(cnt, min_r, max_r))



def brute_force_b(min_r: int, max_r: int):
	# Part B
	cnt = 0
	for v in range(min_r, max_r + 1):
		is_inc, duplicates = check_number(v)

		# Ensure there is a 2-count duplicate

		if is_inc and check_duplicates(duplicates):
			cnt += 1

	print("Counted {} valid passwords in range {}:{}".format(cnt, min_r, max_r))


# brute_force(*password_range)
brute_force_b(*password_range)

