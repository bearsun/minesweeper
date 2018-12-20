from random import shuffle

class mmap():
	""" data structure to create and manipulate the mapping of mine field"""
	def __init__(self):
		"""initiate a new map with 16x16 grid, 40 mines"""
		mmap.n_mines = 40
		mmap.n_rows = 16
		mmap.n_cols = 16
		mmap.field = self.remap(mmap.n_rows, mmap.n_cols, mmap.n_mines)

		# int for open status:
		# 	0 for unopened
		# 	-1 for flagged
		# 	1 for opened
		mmap.open = [[0 for _ in range(mmap.n_cols)] for _ in range(mmap.n_rows)]

		# cursor position
		mmap.cursor_x = 0
		mmap.cursor_y = 0

		# horizontal location of the display
		mmap.ystart = 0

		# mines flagged
		mmap.n_flags = 0

		# mine exploded
		mmap.b_explode = False

		# mines cleaned
		mmap.b_finish = False

	def check(self, x, y, b_field):
		"""check a certain spot at the field

		input
		-----
		int x: row index of the spot
		int y: column index of the spot
		bool[] field: boolean array indicating mine positions

		output
		------
		int status: number of mines in or around current locatoin, see remap
		"""
		nrows, ncols = len(b_field), len(b_field[0])
		if b_field[x][y]:
			return -1
		else:
			n = 0
			for irow in range(x-1, x+2):
				for icol in range(y-1, y+2):
					if -1 < irow < nrows and -1 < icol < ncols:
						if b_field[irow][icol]:
							n += 1
			return n


	def remap(self, n_rows, n_cols, n_mines):
		"""generate a new map

		input
		-----
		int n_rows: number of rows
		int n_cols: number of columns
		int n_mines: number of mines

		output
		------
		int[] field: n_rows X n_cols int array
					   -1: mine
					   0: no mine, no mine around
					   1: no mine, 1 mine around
					   2: no mine, 2 mine around
					   etc......
		"""

		# randomize mine positions
		b_field_1d = [i < n_mines for i in range(n_rows * n_cols)]
		shuffle(b_field_1d)
		b_field = [[b_field_1d[i * n_rows + j] for j in range(n_cols)] for i in range(n_rows)]

		# build mine map
		field = [[None for _ in range(n_cols)] for _ in range(n_rows)]
		for irow in range(n_rows):
			for icol in range(n_cols):
				field[irow][icol] = self.check(irow, icol, b_field)

		return field