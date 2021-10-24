# a fun little program that renders a simple 4D prism keyed off a dynamic
# Thue-Morse sequence keyed off the current (resizable!) terminal dimensions.
# pardon the somewhat ugly (if traditional) characters - it's a WIP ;D
#
# considerably less jank - special thanks to WeekendWarrior1 <3
# 
# dwimmer 2021

import curses, time
from itertools import product

def main():
	'''
		Automates curses housekeeping - thankfully.
	'''
	curses.wrapper(curses_main)


def curses_main(w):
	'''
		Initilises xterm-x256 colours and frame dimensions, hides cursor and 
		disables echo, and starts main loop with live resizing.
		:arg:		w 			curses window object
	'''
	curses.curs_set(0)
	curses.noecho()
	curses.start_color()
	curses.use_default_colors()
	[curses.init_pair(i, i, -1) for i in range(232, 256)]
	w.nodelay(True)

	n, fy, fx = resize(w) 

	while True:	
		if w.getch() == curses.KEY_RESIZE:
			n, fy, fx = resize(w)

		prism(w, n, fy, fx)


def resize(w):
	'''
		Returns current size of terminal and a seed number for Thue-Morse prism.
		:var:		fy, fx		current x and y dimensions of frame/terminal
		:var:		n 			base number relative to terminal dimensions
	'''
	fy, fx = w.getmaxyx()
	n = round((min(fy, fx)-1) // 4)
	return n, fy, fx


def prism(w, n, fy, fx):	
	'''
		Generate slices of a 4D Thue-Morse prism and pass to render().
		:var:		prism		2D array of colour values
		:var:		r 			dimension of prism array
		:var:		timestamp	mark, in nanoseconds, time before processing
	'''
	r = (n*2)-1

	for t in range(n):
		timestamp = time.time_ns()
		prism = [[0 for __ in range(r)] for __ in range(r)]
		for z, y, x in product(range(n), range(n), range(n)):
			if prism[y+z][x+z] >> 5 == 0:
				prism[y+z][x+z] = modulo((t+z+y+x), n) + 32
		render(w, fy, fx, prism, r, timestamp)


def modulo(a, b):
	'''
		Returns modulo arithmetic - allowing for result of zero.
		:arg:		a 			4D prism coordinate
		:arg:		b 			base number relative to terminal dimensions
	'''
	try:
		return a % b
	except ZeroDivisionError:
		return 0	


def render(w, fy, fx, prism, r, timestamp):
	'''
		Erases screen and renders the provided prism slice at centre screen.
	'''
	w.erase()
	w.border('|', '|', '-', '-', '.', '.', "'", "'")
	try:
		for y, x in product(range(r), range(r)):
			if prism[y][x] != 0:
				w.addstr(
						centre(fy, r)+y, 
						centre(fx, r)+x, 
						".", 
						curses.color_pair(232+(prism[y][x]-32))
						)
	except:
		fy, fx = w.getmaxyx()
		render(w, fy, fx, prism, r, timestamp)

	w.refresh()
	curses_sleep(timestamp)


def centre(a, b):
	'''
		Returns 0,0 position of prism relative to current screen centre.
		:arg:		a 			dimension of frame/terminal
		:arg:		b 			dimension of prism array 
	'''
	return (round(a//2) - round(b//2))
    

def curses_sleep(timestamp):
	'''
		Strive for 60 fps regardless of processing time. 
		Initial calculations are all done in nanoseconds.
		:var:		nap 		determines elapsed time since timestamp in ms
	'''
	nap = int(((1000000000 / 60) - (time.time_ns() - timestamp)) // 1000000)
	if nap > 0: curses.napms(nap)



main()
		
