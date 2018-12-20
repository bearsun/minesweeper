#! /usr/bin/env python3
import curses, sys, subprocess
from display import draw_field, print_info, disp_result
from mmap import mmap
from take_resp import take_resp
from curses import wrapper

def minesweeper(stdscr):
	# clear screen
	stdscr.clear()
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
		# resize the window for space
		subprocess.run(['resize', '-s', '40', '80'])
		# wrapper for curses
		wrapper(minesweeper)
	except KeyboardInterrupt:
		sys.exit(0)