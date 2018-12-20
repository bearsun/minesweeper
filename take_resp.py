import curses
def auto_expand(cmap, x, y):
	""" after a cell with no mine around is opened, determine whether it could expand.

	input
	-----
	obj cmap: object with the current state of the minefield
	int x: index of current row
	int y: index of current column

	output
	------
	obj cmap: updated state of the minefield

	"""

	#go ...

	#up
	if x > 0 and cmap.open[x-1][y] == 0: #the cell is unopend and in range 
		cmap.open[x-1][y] = 1 # mark as open
		if cmap.field[x-1][y] == 0: #new cell with no mine around, run auto_expand recursively
			cmap = auto_expand(cmap, x-1, y)
	#left
	if y > 0 and cmap.open[x][y-1] == 0:
		cmap.open[x][y-1] = 1
		if cmap.field[x][y-1] == 0:
			cmap = auto_expand(cmap, x, y-1)
	#down
	if x < cmap.n_rows-1 and cmap.open[x+1][y] == 0:
		cmap.open[x+1][y] = 1
		if cmap.field[x+1][y] == 0:
			cmap = auto_expand(cmap, x+1, y)
	#right
	if y < cmap.n_cols-1 and cmap.open[x][y+1] == 0:
		cmap.open[x][y+1] = 1
		if cmap.field[x][y+1] == 0:
			cmap = auto_expand(cmap, x, y+1)

	#upperleft
	if x > 0 and y > 0 and cmap.open[x-1][y-1] == 0:
		cmap.open[x-1][y-1] = 1
		if cmap.field[x-1][y-1] == 0:
			cmap = auto_expand(cmap, x-1, y-1)
	#upperright
	if x > 0 and y < cmap.n_cols-1 and cmap.open[x-1][y+1] == 0:
		cmap.open[x-1][y+1] = 1
		if cmap.field[x-1][y+1] == 0:
			cmap = auto_expand(cmap, x-1, y+1)
	#lowerleft
	if x < cmap.n_rows-1 and y > 0 and cmap.open[x+1][y-1] == 0:
		cmap.open[x+1][y-1] = 1
		if cmap.field[x+1][y-1] == 0:
			cmap = auto_expand(cmap, x+1, y-1)
	#lowerright
	if x < cmap.n_rows-1 and y < cmap.n_cols-1 and cmap.open[x+1][y+1] == 0:
		cmap.open[x+1][y+1] = 1
		if cmap.field[x+1][y+1] == 0:
			cmap = auto_expand(cmap, x+1, y+1)
	return cmap

def check_map(cmap):
	""" check the current status to see if the user finishes the game successfully

	input
	-----
	obj cmap: object with the current state of the minefield

	output
	------
	bool: True if finished successfully
	"""
	return all([all(row) for row in cmap.open]) and cmap.n_mines == cmap.n_flags

def take_resp(scr, cmap):
	""" wait for keyboard input and then update the current status of the game

	input
	-----
	obj scr: curses window object
	obj cmap: object with the current state of the minefield

	output
	------
	obj cmap: updated state of the minefield
	"""

	# wait for keyboard
	key = scr.getch()

	# initialize offset(row, col) to track cursor movement by arrow keys
	offset = [0, 0]
	if key == curses.KEY_LEFT:
		offset[1] -= 1
	elif key == curses.KEY_RIGHT:
		offset[1] += 1
	elif key == curses.KEY_UP:
		offset[0] -= 1
	elif key == curses.KEY_DOWN:
		offset[0] += 1
	elif key == ord('f'): # put flag on the current cell
		if cmap.open[cmap.cursor_x][cmap.cursor_y] == 0: #only if unopened
			cmap.open[cmap.cursor_x][cmap.cursor_y] = -1 #flagged
			cmap.n_flags += 1
		elif cmap.open[cmap.cursor_x][cmap.cursor_y] == -1: # if already flagged
			cmap.open[cmap.cursor_x][cmap.cursor_y] = 0 #unflag
			cmap.n_flags -= 1
	elif key == ord(' '): # space bar to open a cell
		if cmap.open[cmap.cursor_x][cmap.cursor_y] == 0: #only if unopened
			if cmap.field[cmap.cursor_x][cmap.cursor_y] == -1: #if mine
				cmap.b_explode = True #boooom!
				return cmap
			else:
				cmap.open[cmap.cursor_x][cmap.cursor_y] = 1
				if cmap.field[cmap.cursor_x][cmap.cursor_y] == 0: # no mine around, check if it can auto-expand
					cmap = auto_expand(cmap, cmap.cursor_x, cmap.cursor_y)

	# update cursor position
	cmap.cursor_x = min(max(cmap.cursor_x + offset[0], 0), cmap.n_rows-1) # range 0 to n_rows-1
	cmap.cursor_y = min(max(cmap.cursor_y + offset[1], 0), cmap.n_cols-1) # range 0 to n_cols-1

	# does the user finish successfully?
	cmap.b_finish = check_map(cmap)

	return cmap