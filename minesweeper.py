#! /usr/bin/env python3
import curses, sys
from display import draw_field, print_info, disp_result
from mmap import mmap
from take_resp import take_resp

def minesweeper(stdscr):
	""" play minesweeper in your bash terminal!"""
	
	# hide cursor
	curses.curs_set(0)
	# clear screen
	stdscr.clear()
	curses.resizeterm(30, 50)
	while True:
		# initialize a new mine field with basic parameters
		cmap = mmap()
		while True:
			iline = draw_field(stdscr, cmap)
			print_info(stdscr, cmap, iline)
			cmap = take_resp(stdscr, cmap) #wait and collect response
			stdscr.refresh()
			if cmap.b_explode or cmap.b_finish:
				break
		disp_result(stdscr, cmap)

if __name__== "__main__":
	try:
		# resize the window for space (dosen't work on Mac)
		#subprocess.call(['resize', '-s', '30', '50'])
		# wrapper for curses
		curses.wrapper(minesweeper)
	except KeyboardInterrupt:
		sys.exit(0)
	except curses.error: #not enough space for drawing
		print('Please make your terminal window larger!')
		sys.exit(0)
