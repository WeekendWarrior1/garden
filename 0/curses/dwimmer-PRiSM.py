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
		:var:		my, mx		current max x and y dimensions of terminal
		:var:		n 			base number relative to terminal dimensions
	'''
	curses.curs_set(0)
	curses.noecho()
	curses.start_color()
	curses.use_default_colors()
	[curses.init_pair(i, i, -1) for i in range(232, 256)]
	w.nodelay(True)

	n, my, mx = resize(w) 

	while True:	
		if w.getch() == curses.KEY_RESIZE:
			n, my, mx = resize(w)

		prism(w, n, my, mx, ((n*2)-1))


def resize(w):
	'''
		Returns current size of terminal and a seed number for Thue-Morse prism.
	'''
	my, mx = w.getmaxyx()
	n = round((min(my, mx)-1) // 4)
	return n, my, mx


def prism(w, n, my, mx, pd):	
	'''
		Generate slices of a 4D Thue-Morse prism and pass to render().
		:arg:		pd 			dimension of prism array
		:var:		prism		2D array of colour values
		:var:		timestamp	mark, in nanoseconds, time before processing
	'''
	for t in range(n):
		timestamp = time.time_ns()
		prism = [[32 for __ in range(pd)] for __ in range(pd)]
		for z, y, x in product(range(n), range(n), range(n)):
			if prism[y+z][x+z] >> 5 == 1:
				prism[y+z][x+z] = modulo((t+z-y-x), n)
		render(w, n, my, mx, prism, pd, timestamp)


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


def render(w, n, my, mx, prism, pd, timestamp):
	'''
		Erases screen and renders the provided prism slice at centre screen.
	'''
	w.erase()
	w.border('|', '|', '-', '-', '.', '.', "'", "'")
	try:
		for y, x in product(range(pd), range(pd)):
			if prism[y][x] != 32:
				w.addstr(
						centre(my, pd)+y, 
						centre(mx, pd)+x, 
						".", 
						curses.color_pair(colour(prism[y][x], n))
						)
	except:
		my, mx = w.getmaxyx()
		render(w, n, my, mx, prism, pd, timestamp)

	w.refresh()
	curses_sleep(n, timestamp)


def centre(a, b):
	'''
		Returns 0,0 position of prism relative to current screen centre.
		:arg:		a 			dimension of frame/terminal
		:arg:		b 			dimension of prism array 
	'''
	return (round(a//2) - round(b//2))


def colour(i, n, crs=232, cr=24):
	'''
		Divides the colour range into approximately n spaced values and 
		returns prism index plus colour range start value.
		:arg:		i 			index of prism array
		:arg:		crs 		xterm256 colour range start value
		:arg:		cr 			length of colour range
	'''
	return (crs + round((i * ((cr / n) * 10)) / 10))
    

def curses_sleep(n, timestamp, fr=24):
	'''
		Strive for fr frame rate regardless of processing time. 
		Initial calculations are all done in nanoseconds.
		:arg:		fr 			target frame rate in seconds
		:var:		nap 		determines elapsed time since timestamp in ms
	'''
	nap = int(((1000000000 / fr) - (time.time_ns() - timestamp)) // 1000000)
	if nap > 0: curses.napms(nap)



main()
		
