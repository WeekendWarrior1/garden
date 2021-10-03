# dwimmer 2021

class Sequence:
	''' A simple program to explore (some of) the interesting properties of the
		Thue-Morse sequence. 
	'''
	def __init__(self, time, base):
		self.time = time
		self.base = base
		self.sequence = self.generate()
		self.number_set = [i for i in range(1,len(self.sequence)+1)]

	def generate(self, bus=[]):
		""" Generate a Thue-Morse sequence with user specified base and time 
			values. Utilises modulo to allow base numbers other than 2.
		"""
		sequence = [i % self.base for i in range(self.base)]
		for loop in range(self.time):
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



x = Sequence(3, 2)
print(x.sequence)
for key in range(x.base):
	x.sum_set(key)







