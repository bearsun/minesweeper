import curses
def auto_expand(cmap, x, y):
	#up
	if x > 0 and cmap.open[x-1][y] == 0:
		cmap.open[x-1][y] = 1
		if cmap.field[x-1][y] == 0:
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
	return all([all(row) for row in cmap.open]) and cmap.n_mines == cmap.n_flags

def take_resp(scr, cmap):
	key = scr.getch()
	offset = [0, 0]
	if key == curses.KEY_LEFT:
		offset[1] -= 1
	elif key == curses.KEY_RIGHT:
		offset[1] += 1
	elif key == curses.KEY_UP:
		offset[0] -= 1
	elif key == curses.KEY_DOWN:
		offset[0] += 1
	elif key == ord('f'):
		if cmap.open[cmap.cursor_x][cmap.cursor_y] == 0: #only if unopened
			cmap.open[cmap.cursor_x][cmap.cursor_y] = -1 #flagged
			cmap.n_flags += 1
		elif cmap.open[cmap.cursor_x][cmap.cursor_y] == -1: # if already flagged
			cmap.open[cmap.cursor_x][cmap.cursor_y] = 0 #unflag
			cmap.n_flags -= 1
	elif key == ord(' '):
		if cmap.open[cmap.cursor_x][cmap.cursor_y] == 0: #only if unopened
			if cmap.field[cmap.cursor_x][cmap.cursor_y] == -1: #if mine
				cmap.b_explode = True
				return cmap
			else:
				cmap.open[cmap.cursor_x][cmap.cursor_y] = 1
				if cmap.field[cmap.cursor_x][cmap.cursor_y] == 0:
					cmap = auto_expand(cmap, cmap.cursor_x, cmap.cursor_y)

	cmap.cursor_x = min(max(cmap.cursor_x + offset[0], 0), cmap.n_rows-1) # range 0 to n_rows-1
	cmap.cursor_y = min(max(cmap.cursor_y + offset[1], 0), cmap.n_cols-1) # range 0 to n_cols-1

	cmap.b_finish = check_map(cmap)
	return cmap