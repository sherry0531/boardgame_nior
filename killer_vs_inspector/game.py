import string, random
import numpy as np

# init evidence_deck
self.evidence_deck = list(string.ascii_lowercase[0:-1])
random.shuffle(self.evidence_deck)


class board:
	def __init__(self):
		suspects = list(string.ascii_lowercase[0:-1])
		random.shuffle(suspects)
		# convert board to a 5*5 list of list
		row = []
		self.board = []
		for i in suspects:
			if len(row) != 5:
				row += [i]
			if len(row) == 5:
				self.board += [row]
				row = []
	def show(self):
		# print aligned grid (there will be a, a_dead, a_innocent)
		longest_name = 'a_innocent'
		print_board = ''
		for row in self.board:
			for person in row:
				if len(person) < len(longest_name):
					person = person + " " * (len(longest_name) - len(person))
				print_board += person
			# add new line for each row
			print_board += '\n'
		print(print_board)
	
	def shift(self):
		pass

	def collapse(self):
		pass
		


def show_and_hide(name):
	# show name on the screen, and hide it. confirm if hide
	if len(name.split()) > 0:
		show = 'evidence_hand'
	else:
		show = 'identity'
	input(f"Press enter to see your {show}. Proceed only when nobdoy but you are looking at the screen...")
	print(name)
	input(f"Press enter to hide your {show}...")
	print("\n" * 1000)
	hide = input(f'Is your {show} safely hidden from the screen? y/n')
	while hide != 'y':
		print("\n" * 1000)
		hide = input(f'Now is your {show} safely hidden from the screen? Please enter y/n')

def adjacent(person, board):
	# return a list of adjacent suspects for selected person
	board = np.array(board)
	index_row, index_col = np.where(board == person)
	row_max = min(index_row[0] + 1, board.shape[0] -1) 
	row_min = max(index_row[0] - 1, 0)
	col_max = min(index_col[0] + 1, board.shape[1] -1)
	col_min = max(index_col[0] - 1, 0)
	adjacent_lst = []
	for row in range(row_min, row_max+1):
		for col in range(col_min, col_max+1):
			if board[row][col] != person:
				adjacent_lst += [board[row][col]]
	return(adjacent_lst)

	
		
class killer(player):
	def __init__(self, evidence_deck):
		self.name = input("Welcome ! Please enter your name: ")
		self.identity = evidence_deck.pop(0)
		show_and_hide(self.identity)

	def kill(self, board, inspector):
		victim = input('Please enter the name of suspect you want to kill... (you can only kill an adjacent suspect. Killing an innocent suspect will canvas inspector.): ')
		try:
			adjacent_suspects = adjacent(self.identity, board)
		except:
			print('Attempted to kill an unknown, dead or innocent suspect! Please choose a suspect from %s. If killing innocent suspect, please type "name_innocent". e.g. "a_innocet"' % ([person for row in board for person in row]))
			victim, board = self.kill(board, inspector)
		while victim not in adjacent_suspects:
			victim = input('Attempted to kill a suspect that is not adjacent to killer! Please choose adjacent suspect to kill! Enter the name of suspect you want to kill...: ')
		while 'dead' in victim:
			victim = input("Can't kill a dead suspect! Please choose a different suspect to kill. Enter the name of suspect you want to kill...: ")
		if 'innocent' in victim:
			# canvas inspector
			adjacent_suspects = adjacent(victim, board)
			if inspector in adjacent_suspects:
				print('Inspector is adjacent to the killed innocent suspect!')
			else:
				print("Inspector is not adjacent to the killed innocent suspect")
		if victim == inspector:
			print('Inspector dead! Killer Win!')
			exit()
		# mark kill to "dead" on the board
		board = np.array(board)
		board[board == victim] = (victim + '_dead').replace('_innocent', '')
		board = board.tolist()
		return(board)
	
	def disguise(self, board, evidence_deck):
		card = evidence_deck.pop(0)
		show_and_hide(card)
		if card in [person for row in board for person in row]:
			board = np.array(board)
			board[board == self.identity] = self.identity + '_innocent'
			board = board.tolist()
			print('killer disguise successed! %s now is innoced' % (self.killer))
			self.identity = card
		else:
			print('killer disguise failed!')
		return(board, evidence_deck)
			



class inspector:
	def __init__(self, evidence_deck):
		self.name = input("Welcome ! Please enter your name: ")
		self.evidence_hand = [evidence_deck.pop(0)] + [evidence_deck.pop(0)] + [evidence_deck.pop(0)] + [evidence_deck.pop(0)] 
		show_and_hide(self.evidence_hand)
		self.identity = input("Please select one from evidence hand to be your identity: ")
		while self.identity not in self.evidence_hand:
			self.identity = input('Selected person not in evience hand! Please select one from evidence hand: ')
		show_and_hide(self.identity) 
 
	def accuse(self, board, killer):
		accused_suspect = input('Please enter the name of suspect you want to accuse... (you can only accuse an adjacent suspect.)') 
		try:
			adjacent_suspects = adjacent(self.identity, board)
		except:
			print('Attempted to accuse an unknown, dead or innocent suspect! Please choose a suspect from %s. ' % ([person for row in board for person in row]))
			accused_suspect = self.accuse(board, killer)
		if accused_suspect not in adjacent_suspects:
			print('Attempted to accuse a suspect that is not adjacent to inspector! Please choose adjacent suspect to accuse')
			accused_suspect = self.accuse(board, killer)
		if ('dead' in accused_suspect)|('innocent' in accused_suspect):
			print("Attempted to accuse a dead or innocent suspect! Please choose a different adjacent suspect from %s .' % ([person for row in board for person in row])
			accused_suspect = self.accuse(board, killer)
		if accused_suspect == killer:
			print('Killer accused! Inspector win!')
			exit()
		return()

	def exonerate(self, evidence_deck, board, killer):
		self.evidence_hand += [evidence_deck.pop(0)]
		show_and_hide(self.evidence_hand)
		discard = input('Please discard a suspect from your hand. Enter the name of discarded suspect: ')
		while discard not in self.evidence_hand:
			discard = input('Discarded suspect not in your hand! please select a card from your hand to discard: ')
		board = np.array(board)
		if len(board[board == discard]) == 1:
			board[board == discard] = discard + '_innocent'			
			adjacent_suspects = adjacent(discard + '_innocent', board)
			if killer in adjacent_suspects:
				print(f'Killer is adjacent to {discard}!') 
			else:
				print(f'Killer is not adjacent to {discard}')
		return(evidence_deck, board)

			
					
