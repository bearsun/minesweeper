def draw_row(scr, cmap, irow, iline):
	line = []
	for icol in range(cmap.n_cols):
		cur = ' '
		if cmap.open[irow][icol] ==  1: # opened
			if cmap.field[irow][icol] == 0:
				cur += ' ' #empty
			elif cmap.field[irow][icol] == -1:
				cur += '*'
			else:
				cur += str(cmap.field[irow][icol]) #number of mines
		elif cmap.open[irow][icol] == 0: # unopened
			cur += '█'
		elif cmap.open[irow][icol] == -2:
			cur += 'X'
		else:
			cur += '@' # flagged
		cur += ' '
		line.append(cur)

	# add cursor
	if cmap.cursor_x == irow:
		line[cmap.cursor_y] = '[' + line[cmap.cursor_y][1] + ']'

	strline = '│' + '│'.join(line) + '│'
	scr.addstr(iline, cmap.ystart, strline)
	return iline + 1

def draw_field(scr, cmap):
	""" draw the mine field in the terminal. """
	width = cmap.n_cols
	# borders / lines
	topline = '┌' + '┬'.join(['───'] * width) + '┐'
	midline = '├' + '┼'.join(['───'] * width) + '┤'
	botline = '└' + '┴'.join(['───'] * width) + '┘'

	# index for current line
	iline = 0

	# draw top border
	scr.addstr(iline, cmap.ystart, topline)
	iline += 1

	# draw the rest
	for irow in range(cmap.n_rows):
		# draw row with mines
		iline = draw_row(scr, cmap, irow, iline)
		# draw mid/bottom line
		if irow != cmap.n_rows-1:
			scr.addstr(iline, cmap.ystart, midline)
		else:
			scr.addstr(iline, cmap.ystart, botline)
		iline += 1

	return iline

def print_info(scr, cmap, iline):
	# print information
	scr.addstr(iline, cmap.ystart, \
		'flags: '+ str(cmap.n_flags) + '\t'\
		+ 'mines: ' + str(cmap.n_mines-cmap.n_flags))
	iline += 1
	scr.addstr(iline, cmap.ystart, 'Space: open    F: flag    Ctrl+C: quit')
	return

def disp_result(scr, cmap):
	for irow in range(cmap.n_rows):
		for icol in range(cmap.n_cols):
			if cmap.open[irow][icol] == 0:
				cmap.open[irow][icol] = 1
			elif cmap.open[irow][icol] == -1:
				if cmap.field[irow][icol] != -1:
					cmap.open[irow][icol] = -2
	iline = draw_field(scr, cmap)
	if cmap.b_explode:
		scr.addstr(iline, cmap.ystart, 'Boooooom!\n')
	else:
		scr.addstr(iline, cmap.ystart, 'Congradulation!\n')
	iline += 1
	scr.addstr(iline, cmap.ystart, 'Press any key to restart.\n')
	scr.getch()