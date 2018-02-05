# Input from the text file & parse the horizontal holes
# Hole format: [x_init, y_init, is_accross, length, supposed_content]
file_name = input("Enter the input file name: ")
input = open(file_name)
dimension = int(input.readline())
table = list()
holes = list()
for row in range(dimension):
	table.append(list(input.readline())[:-1])
	found = False
	for column in range(dimension):
		if found:
			if table[row][column] == "-": length += 1
			if table[row][column] != "-" or column == dimension - 1:
				found = False
				if length > 1 : holes.append([x_init, y_init, True, length, ""])
				length = 0
		else:
			if table[row][column] == "-":
				found = True
				length = 1 
				x_init = column
				y_init = row
words = input.readline().split(";")
words.sort(key = len, reverse = True)

# Parse the vertical holes
for column in range(dimension):
	found = False
	for row in range(dimension):
		if found:
			if table[row][column] == "-": length += 1
			if table[row][column] != "-" or row == dimension - 1:
				found = False
				if length > 1 : holes.append([x_init, y_init, False, length, ""])
				length = 0
		else:
			if table[row][column] == "-":
				found = True
				length = 1 
				x_init = column
				y_init = row
holes.sort(key = lambda x: x[3], reverse = True)

# Define fill function
def fill(x_init, y_init, is_accross, word_as_list):
	global table
	for i in range(len(word_as_list)):
		if is_accross:
			table[y_init][x_init+i] = word_as_list[i]
		else:
			table[y_init+i][x_init] = word_as_list[i]

# Define is_valid, if the words are unchanged from the suppossed word (see the comment on holes)
def is_valid():
	global table, holes
	for hole in holes:
		if len(hole[4]) != 0:
			for i in range(hole[3]):
				if hole[2]:
					if table[hole[1]][hole[0] + i] != list(hole[4])[i]: return False
				else:
					if table[hole[1] + i][hole[0]] != list(hole[4])[i]: return False
	return True

# Undo stack: [x_init, y_init, is_accross, word_as_list]
undo_stack = list()

# Reccursive solve
def solve():
	global table, holes, words, undo_stack
	if not words: return True   # all words have been placed
	for hole in holes:
		for word in words:
			if len(word) == hole[3] and len(hole[4]) == 0:
				# record for undo
				before = list()
				for i in range(hole[3]): 
					before.append(table[hole[1]][hole[0] + i]) if hole[2] else before.append(table[hole[1] + i][hole[0]])					
				undo_stack.append([hole[0], hole[1], hole[2], before])
				# fill
				word_idx = words.index(word)
				fill(hole[0], hole[1], hole[2], list(words.pop(word_idx)))
				hole_idx = holes.index(hole)
				holes[hole_idx][4] = word
				# if the current content is valid and the children are valid
				if is_valid() and solve(): return True 
				# undo
				words.insert(word_idx, word)				
				holes[hole_idx][4] = ""
				before = undo_stack.pop()
				fill(before[0], before[1], before[2], before[3])	
		# Try other holes?
	return False

# The brute force algorithm
import time
start = time.time()
solve()
start = time.time() - start

# Output
printable = str()
print()
for row in table:
	print(printable.join(row))
	printable = ""
print("\nThat took %s second(s)\n" %(start))