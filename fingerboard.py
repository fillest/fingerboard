import itertools
import argparse
import re


class fg:
	BLACK   = '\033[30m'
	RED     = '\033[31m'
	GREEN   = '\033[32m'
	YELLOW  = '\033[33m'
	BLUE    = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN    = '\033[36m'
	WHITE   = '\033[37m'
	RESET   = '\033[39m'
	DARK_GRAY   = '\033[90m'

class bg:
	BLACK   = '\033[40m'
	RED     = '\033[41m'
	GREEN   = '\033[42m'
	YELLOW  = '\033[43m'
	BLUE    = '\033[44m'
	MAGENTA = '\033[45m'
	CYAN    = '\033[46m'
	WHITE   = '\033[47m'
	RESET   = '\033[49m'

class style:
	BRIGHT    = '\033[1m'
	DIM       = '\033[2m'
	NORMAL    = '\033[22m'
	RESET_ALL = '\033[0m'

def main():
	cli_parser = argparse.ArgumentParser()
	cli_parser.add_argument('--scales', action = 'store_true', help = "just show supported scales")
	cli_parser.add_argument('--tunings', action = 'store_true', help = 'just show built-in tunings')
	cli_parser.add_argument('--tuning', default = 'guitar', help = 'e.g. guitar or "ga#c#ega#"')
	cli_parser.add_argument('--scale', default = 'major', help = "scale name, use --scales to show available")
	cli_parser.add_argument('--tonic', default = 'c', help = 'tonic note, e.g. c or "a#"')
	cli_parser.add_argument('--chord', default = '', help = "e.g. c or am7")
	cli_parser.add_argument('--fingerboard-length', default = 24, type = int)
	cli_args = cli_parser.parse_args()

	if cli_args.chord:
		tonic = cli_args.chord.lower()[0] #TODO parse accidentals
	else:
		tonic = cli_args.tonic.lower()
	fingerboard_length = cli_args.fingerboard_length
	scale = cli_args.scale

	all_chromatic_notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

	assert cli_args.tonic in all_chromatic_notes

	# class major:
	# 	def __init__(self, tonic):
	# 		self.tonic = tonic

	# 	def notes(self):
	# 		chromatic_notes_from_tonic = itertools.dropwhile(lambda note: note != self.tonic, itertools.cycle(all_chromatic_notes))
	# 		scale_notes = []
	# 		for interval in [0] + [whole, whole, half, whole, whole, whole, half]:
	# 			for _ in range(interval):
	# 				next_note = next(chromatic_notes_from_tonic)
	# 			scale_notes.append(next_note)

	# 		# assert scale_notes[-1] == tonic
	# 		# scale_notes.pop()

	# class ScaleDegree:
	# 	def __init__(self, number):
	# 		self.number = number
	# 		self.mod_flat = False
	# 		self.mod_sharp = False

	# 	def flat(self):
	# 		self.mod_flat = True

	# 	def sharp(self):
	# 		self.mod_sharp = True
	# D = ScaleDegree

	# class minor(major):
	# 	degrees = [D(1), D(2), D(3).flat(), D(4), D(5), D(6).flat(), D(7).flat(), D(8)]

	# class anchi_hoye(major):
	# 	degrees = [D(1), D(3).flat(), D(4).sharp(), D(5), D(7)]

	scales = {}
	scales['major'] = [2, 2, 1, 2, 2, 2, 1]  #https://en.wikipedia.org/wiki/Major_scale 	#aka ionian
	scales['dorian'] = [2, 1, 2, 2, 2, 1, 2]
	scales['phrygian'] = [1, 2, 2, 2, 1, 2, 2]
	scales['lydian'] = [2, 2, 2, 1, 2, 2, 1]
	scales['mixolydian'] = [2, 2, 1, 2, 2, 1, 2]
	scales['locrian'] = [1, 2, 2, 1, 2, 2, 2]
	#https://en.wikipedia.org/wiki/Minor_scale#Relationship_to_parallel_major
	scales['minor'] = [2, 1, 2, 2, 1, 2, 2]  #https://en.wikipedia.org/wiki/Minor_scale
	#         Natural minor, aka Aeolian
	#https://www.youtube.com/watch?v=13DgDatNg8A&t=158s
	#https://youtu.be/EltgjHLTZ_s?t=50
	scales['harmonic_minor'] = [2, 1, 2, 2, 1, 3, 1]
	scales['melodic_minor'] = [2, 1, 2, 2, 2, 2, 1]
	scales['anchihoye'] = [1, 4, 1, 3, 3]
	scales['tizita_minor'] = [2, 1, 4, 1, 4]  #https://ianring.com/musictheory/scales/397
	scales['bati_minor'] = [3, 3, 1, 4, 1]
	scales['major_pentatonic'] = [2, 2, 3, 2, 3]
	scales['minor_pentatonic'] = [3, 2, 2, 3, 2]
	scales['blues_minor'] = [3, 2, 1, 1, 3, 2]
	scales['whole_tone'] = [2, 2, 2, 2, 2, 2]
	#https://en.wikipedia.org/wiki/Pentatonic_scale
	#TODO https://www.guitarscale.org/a.html

	#strings: Nth to 1st
	built_in_tunings = {
		'guitar': ['e', 'a', 'd', 'g', 'b', 'e'],  #e2 a2 d3 g3 b3 e4
		'guitar_bass': ['e', 'a', 'd', 'g'],  #e1 a1 d2 g2

		'piano': ['c'],
		
		'cello': ['c', 'g', 'd', 'a'],  #c2 g2 d3 a3
		'cello_p4_high': ['f#', 'b', 'e', 'a'],  #perfect fourths (five semitones) (1st stays A)
		'cello_p4_2': ['e', 'a', 'd', 'g'],  #(2nd stays D) -- E2 A2 D3 G3 (same as guitar standard)

		'violin': ['g', 'd', 'a', 'e'],  #g3 d4 a4 e5
		'violin5_low': ['c', 'g', 'd', 'a', 'e'],
		'violin_p4_high': ['c#', 'f#', 'b', 'e'],  #perfect fourths (five semitones) like guitar (1st stays E)
	}
	strings = built_in_tunings.get(cli_args.tuning) or re.findall(r'[a-z]#?', cli_args.tuning)

	if cli_args.tunings:
		for name, notes in built_in_tunings.items():
			print(name, notes)
		return

	if cli_args.scales:
		for name in scales:
			print(name)
		return
	
	if cli_args.chord:
		print(f"chord: {cli_args.chord}")
	else:
		print(f"scale: {tonic.upper()} {scale}")
	

	# colors = [BG_RED, fg.RED, fg.GREEN, fg.YELLOW, fg.MAGENTA, fg.CYAN, style.RESET_ALL]
	# colors = [bg.RED, bg.RED, bg.GREEN, bg.YELLOW, bg.MAGENTA, bg.CYAN, style.RESET_ALL]

	def scale_to_degree(tonic, name, degree):
		if degree == 1:
			return tonic

		notes_from_tonic = itertools.dropwhile(lambda note: note != tonic, itertools.cycle(all_chromatic_notes))

		next(notes_from_tonic)  #consume tonic
		i = 2
		for interval in itertools.cycle(scales[name]):
			for _ in range(interval):
				next_note = next(notes_from_tonic)
			if i == degree:
				return next_note
			i += 1

	notes_from_tonic = itertools.dropwhile(lambda note: note != tonic, itertools.cycle(all_chromatic_notes))
	next(notes_from_tonic)  #consume tonic
	scale_notes = [tonic]
	if cli_args.chord:
		if len(cli_args.chord) == 1:
			scale_notes.append(scale_to_degree(tonic, 'major', 3))
			scale_notes.append(scale_to_degree(tonic, 'major', 5))
		else:
			if cli_args.chord[1] == 'm':
				scale_notes.append(scale_to_degree(tonic, 'minor', 3))
				scale_notes.append(scale_to_degree(tonic, 'minor', 5))
				if cli_args.chord.endswith('7'):
					scale_notes.append(scale_to_degree(tonic, 'minor', 7))
				if cli_args.chord.endswith('9'):
					scale_notes.append(scale_to_degree(tonic, 'minor', 7))
					scale_notes.append(scale_to_degree(tonic, 'minor', 9))
			else:
				scale_notes.append(scale_to_degree(tonic, 'major', 3))
				scale_notes.append(scale_to_degree(tonic, 'major', 5))
				if cli_args.chord.endswith('7'):
					scale_notes.append(scale_to_degree(tonic, 'minor', 7)) #Dominant 7th (aka just a 7th), not Xmaj7|XM7|XΔ7 -- major chord with a MINOR 7th
				if cli_args.chord.endswith('9'):
					scale_notes.append(scale_to_degree(tonic, 'minor', 7))
					scale_notes.append(scale_to_degree(tonic, 'major', 9))
	else:
		intervals = scales[scale]
		for interval in intervals:
			for _ in range(interval):
				next_note = next(notes_from_tonic)
			scale_notes.append(next_note)
	# assert scale_notes[-1] == tonic
	# scale_notes.pop()
	
	# note_to_color = dict(itertools.zip_longest(scale_notes, colors, fillvalue=style.RESET_ALL))

	scale_source = "chord" if cli_args.chord else "scale"
	print(f"{scale_source} notes: {' '.join(n.upper() for n in scale_notes)}")
	# print(f"scale notes: {' '.join((note_to_color[note] + note.upper() + style.RESET_ALL) for note in scale_notes)}")

	print()

	for string_i, open_string_note in enumerate(reversed(strings)):
		all_notes_cycle = itertools.cycle(all_chromatic_notes)
		notes_on_string = itertools.dropwhile(lambda note: note != open_string_note, all_notes_cycle)
		print(f"{fg.DARK_GRAY}{string_i + 1}{style.RESET_ALL}", "    ", end='')
		for i, note in enumerate(itertools.islice(notes_on_string, 1 + fingerboard_length)):
			color = fg.DARK_GRAY
			# color = fg.WHITE + style.DIM
			# color = fg.WHITE
			# color = note_to_color[note]
			color_reset = style.RESET_ALL
			if note in scale_notes:
				color = style.BRIGHT + fg.RED if note == tonic else style.RESET_ALL
				# color = bg.WHITE + note_to_color[note]
				# color = fg.WHITE + note_to_color[note]
				color_reset = style.RESET_ALL
			if i == 0:     #i % 12 == 0
				sep = ' | '
			else:
				sep = '  '
			print(f"{color}{note.upper(): <2}{color_reset}{sep}", end='')
		print()
	
	start = " " * 14
	print()
	print(" " * 11 + ' '.join(f"{i: <3}" for i in range(1, cli_args.fingerboard_length + 1)))

	# #cello positions
	# #https://thecellocompanion.info/tag/cello-position-diagram/
	# if cli_args.tuning == 'cello':
	# 	print(start + '1' * 14)
	# 	print(start + " " * 12 + '3' * 14)
	# 	print(start + " " * 20 + '4' * 14)

if __name__ == '__main__':
	main()
