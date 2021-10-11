# A simple program to explore (some of) the interesting properties of the
# Thue-Morse sequence.
#
# dwimmer 2021

import operator
from PIL import Image, ImageDraw, ImageOps


ops = {
	"+": operator.add,
	"-": operator.sub
	}


class Sequence:
	'''
		A simple program to explore (some of) the interesting properties of the
		Thue-Morse sequence. 
	'''
	def __init__(self, base, time, index, op="+"):
		""" 
		
		"""
		self.base = base
		self.time = time 
		self.index = index
		self.op = op
		self.name = f'n{self.base}t{self.time}i{self.index}'

	def generate(self, sequence, duration):
		"""
			Generate a Thue-Morse sequence with user specified base and time 
			values. Utilises modulo to allow base numbers other than 2.
		"""
		for loop in range(duration):
			bus = []
			for e in sequence:
				for i in range(self.base):
					bus.append((i+e) % self.base)
			sequence = []
			sequence.extend(bus)			
		return sequence

	def draw_base(self, sequence, sequence_square):
		"""
		"""
		d = len(sequence)
		image = Image.new("RGB",(d, d))
		draw = ImageDraw.Draw(image)
		for y in range(d):
			for x in range(d):
				hue = 268
				saturation = 100
				lightness = (sequence_square[(y+x)]*(100/self.base)) % 100
				draw.point((x,y), f'hsl({hue},{saturation}%,{lightness}%)')		
		return image

	def draw_symmetry(self, base_image):
		"""
		"""
		d = base_image.width
		image = Image.new("RGB", (d * 2, d * 2))
		draw = ImageDraw.Draw(image)
		image.paste(base_image, (0, 0))
		image.paste(ImageOps.mirror(base_image), (d, 0))
		image.paste(ImageOps.flip(base_image), (0, d))
		image.paste(ImageOps.mirror(ImageOps.flip(base_image)), (d, d))
		return image

	def groups(self):
		"""
			Iterates over the generated Thue-Morse sequence, creating balanced 
			groups of integers - demonstrating the balance and beauty of this
			particular sequence.
		"""
		groups = {key: None for key in [i for i in range(self.base)]}
		for k,e in zip(
			self.sequence, 
			[i for i in range(1, len(self.sequence))]
			):
			groups[k].append(e)
		return groups

	def run(self):
		"""
		"""
		sequence = self.generate(
			[ops[self.op](i, self.index) % self.base for i in range(self.base)], 
			(self.time - 1)
			)
		sequence_square = self.generate(
			sequence, 
			self.time
			)	
		base_image = self.draw_base(sequence, sequence_square)
		symmetry_image = self.draw_symmetry(base_image)
		symmetry_image.save(f'{self.name}.png', "PNG")
			

def main():	
	"""
	"""
	n = int(input('base?: '))
	t = int(input('time?: '))
	sequences = {f'{n}{t}{i}': Sequence(n, t, i) for i in range(n)}
	for e in sequences:
		sequences[e].run()

if __name__ == "__main__":
	main()





