# dwimmer 2021
import sys
from PIL import Image, ImageDraw

class Sequence:
	''' A simple program to explore (some of) the interesting properties of the
		Thue-Morse sequence. 
	'''
	def __init__(self, time, base):
		self.time = time 
		self.base = base
		self.sequence = self.generate([i % self.base for i in range(self.base)], self.time)
		self.sequence_square = self.generate(self.sequence, (self.time + 1))
		self.number_set = [i for i in range(1,len(self.sequence)+1)]

	def generate(self, sequence, length):
		""" Generate a Thue-Morse sequence with user specified base and time 
			values. Utilises modulo to allow base numbers other than 2.
		"""
		bus = []
		for loop in range(length):
			for e in sequence:
				for i in range(self.base):
					bus.append((i+e) % self.base)
			sequence = []
			sequence.extend(bus)
			bus = []
		return sequence			

	def sum_set(self, key, bus=[]):
		""" Iterates over the generated Thue-Morse and linear number sequences,
			creating balanced sets of integers that are then power summed - 
			demonstrating the balance and beauty of this particular sequence.
		"""
		bus = []
		for k,e in zip(self.sequence, self.number_set):
			if k == key:
				bus.append(e)
		print(bus)
		print('(n + n...) = ' + str(sum(bus)))
		for power in range(self.time):
			sum_set = 0
			for i in bus:
				sum_set += pow(i, power)
			print('(n^' + str(power) + ' n^' + str(power) + '...) = ' + str(sum_set))



		

def divide(a, b):
	try:
		return a / b
	except ZeroDivisionError:
		return 0



# please ignore the below ugliness, it's just scratchpad stuff atm





	

x = Sequence(5, 3)
#print(x.sequence)
for key in range(x.base):
	x.sum_set(key)
print(x.sequence)
print(x.sequence_square)
dx = 0
dy = 0
dimension = len(x.sequence)
print(dimension)
im = Image.new("RGB",(dimension, dimension))
draw = ImageDraw.Draw(im)
for e in x.sequence_square:
	draw.point((dx,dy), 'hsl({},100%,50%)'.format(divide(360,e)))
	dx += 1
	if dx == (dimension):
		dy += 1
		dx = 0
	#dx += 1



im.save("test.png", "PNG")





