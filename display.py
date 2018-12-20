""" all functions related to display in terminal"""

def draw_row(scr, cmap, irow, iline):
	""" draw a row of the minefield

	input
	-----
	obj scr: curses window object
	obj cmap: object with the current state of the minefield
	int irow: index of the row to show in the minefield
	int iline: index of the line position to draw in terminal

	output
	------
	int inline: index of the next line position to draw in terminal
	"""

	# build a list of cells to show
	line = []
	for icol in range(cmap.n_cols):
		cur = ' '
		if cmap.open[irow][icol] ==  1: # opened
			if cmap.field[irow][icol] == 0:
				cur += ' ' #empty & no mine around
			elif cmap.field[irow][icol] == -1:
				cur += '*' #mine
			else:
				cur += str(cmap.field[irow][icol]) #number of mines around
		elif cmap.open[irow][icol] == 0: # unopened
			cur += '█' #covered
		elif cmap.open[irow][icol] == -2: # flagged with no mine
			cur += 'X' #flag wrong, will show only if a mine explodes, see disp_result
		else:
			cur += '@' # flagged
		cur += ' '
		line.append(cur)

	# add [ ] to indicate current cursor position
	if cmap.cursor_x == irow:
		line[cmap.cursor_y] = '[' + line[cmap.cursor_y][1] + ']'

	# add | and build the line
	strline = '│' + '│'.join(line) + '│'
	scr.addstr(iline, cmap.ystart, strline)

	# ready to draw the next line
	return iline + 1

def draw_field(scr, cmap):
	""" draw the mine field in the terminal.

	input
	-----
	obj scr: curses window object
	obj cmap: object with the current state of the minefield

	output
	------
	int inline: index of the next line position to draw in terminal

	"""

	# borders / lines
	topline = '┌' + '┬'.join(['───'] * cmap.n_cols) + '┐'
	midline = '├' + '┼'.join(['───'] * cmap.n_cols) + '┤'
	botline = '└' + '┴'.join(['───'] * cmap.n_cols) + '┘'

	# index for the current line position in terminal
	iline = 0

	# draw the top border
	scr.addstr(iline, cmap.ystart, topline)
	iline += 1

	# draw the rest
	for irow in range(cmap.n_rows):
		# draw the row with mines
		iline = draw_row(scr, cmap, irow, iline)
		# draw mid/bottom line/seperator
		if irow != cmap.n_rows-1: #if not last row, draw midline
			scr.addstr(iline, cmap.ystart, midline)
		else:
			scr.addstr(iline, cmap.ystart, botline)
		iline += 1

	return iline

def print_info(scr, cmap, iline):
	"""print information below the field area: current No. flags, No. mines left

	input
	-----
	obj scr: curses window object
	obj cmap: object with the current state of the minefield
	int iline: index of the line position to draw in terminal

	output
	------
	void
	"""

	# print No. flags and No. mines left
	scr.addstr(iline, cmap.ystart, \
		'Flags: '+ str(cmap.n_flags) + '    '\
		+ 'Mines: ' + str(cmap.n_mines-cmap.n_flags) + '    ← → ↑ ↓: move')
	iline += 1
	# instructions
	scr.addstr(iline, cmap.ystart, 'Space: open    F: flag    Ctrl+C: quit')
	return

def disp_result(scr, cmap):
	""" After completion or explosion, show the whole field

	input
	-----
	obj scr: curses window object
	obj cmap: object with the current state of the minefield
	
	output
	------
	void
	"""

	# go over the field to compare user marking (cmap.open) with true map (cmap.field)
	for irow in range(cmap.n_rows):
		for icol in range(cmap.n_cols):
			if cmap.open[irow][icol] == 0:
				cmap.open[irow][icol] = 1 #reveal unopened area
			elif cmap.open[irow][icol] == -1:
				if cmap.field[irow][icol] != -1:
					cmap.open[irow][icol] = -2 #reveal where the flag marked is wrong

	# draw the mine field
	iline = draw_field(scr, cmap)

	# indicate success or fail
	if cmap.b_explode:
		scr.addstr(iline, cmap.ystart, 'Boooooom!\n')
	else:
		scr.addstr(iline, cmap.ystart, 'Congratulation!\n')
	iline += 1

	# wait for keypress to restart
	scr.addstr(iline, cmap.ystart, 'Press any key to restart.\n')
	scr.getch()
	return