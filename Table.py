from Card import Card
from Player import Player
from random import shuffle
from collections import deque

class Table:
	def __init__(self):
		self.rank_list = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
		self.suit_list = ["H","C","D","S"]

		#list of players in the game
		self.players = []
		#cards on the table
		self.__cards = []

		#highest bet on the table. must be matched to call
		self.__bet = 0

		self.__start_chips = 1000
		self.__big_blind = 0

		#which player is dealer
		self.dealer = 0

		self.setup()

	def get_cards(self):
		return self.__cards
	
	def get_bet(self):
		return self.__bet

	def raise_bet(self, bet):
		#used when someone raises
		self.__bet = self.__bet + bet

	def get_player_cards(self, i):
		return self.players[i].get_player_cards()
	
	def set_player_cards(self,i, card1, card2):
		assert type(card1) == Card, "must be Card class"
		assert type(card2) == Card, "must be Card class"
		self.players[i].set_player_cards(card1, card2)

	def create_deck(self):		
		deck = []
		for suit in self.suit_list:
			for rank in self.rank_list:
				card = Card(rank,suit)
				deck.append(card)
		return deck

	def round(self):
		print("Round Starting...")
		#increments dealer at the start of each round
		self.dealer = (self.dealer + 1) % len(self.players)
		deck = self.create_deck()
		shuffle(deck)

		self.__bet = self.__big_blind

		#person behind dealer is big blind, bet is raised
		self.players[(self.dealer + 1) % len(self.players)].add_bet(self.__big_blind)
		#person behind dealer is little blind.
		self.players[(self.dealer + 2) % len(self.players)].add_bet(self.__big_blind //2)

		turn_index = (self.dealer + 3) % len(self.players)

		#list of all players still playing this round
		active_players = self.players.copy()

		self.deal_cards(deck)
		print("Cards have been dealt to players.")
		print("Big blind for this round is %i chips." % (self.__big_blind))
		#NEED TO CHECK FOR WHEN SOMEONE WINS

		if self.handle_turns(active_players):
			return

		#deal flop, burn 1 card
		deck.pop()
		for i in range(3):
			self.__cards.append(deck.pop())
		print("The flop has been dealt, and the cards on the table are:")
		print(self.display_cards)

		if self.handle_turns(active_players):
			return

		#deal turn
		deck.pop()
		self.__cards.append(deck.pop())
		print("The turn has been dealt, and the cards on the table are:")
		print(self.display_cards)

		if self.handle_turns(active_players):
			return

		#deal river
		deck.pop()
		self.__cards.append(deck.pop())
		print("The river has been dealt, and the cards on the table are:")
		print(self.display_cards)

		if self.handle_turns(active_players):
			return

		#showdown
		
	def handle_turns(self, players):
		"""
		handles asking each player for their turn
		and parses their response accordingly
		until only 1 remains or all have called the bet
		PLAYER.TURN RAISES THEIR BET
		Returns whether or not the round should continue, or if one player has won.
		"""
		playing = True
		while playing:
			for player in players:
				if not player.played or player.get_bet() < self.__bet:
					move = player.turn(self)
					if move == "F":
						players.remove(player)
					elif move[0] == "R":
						#takes raise amount from move str
						num = int(move.split("R")[1])
						self.raise_bet(num)
					player.played = True

		for player in players:
			#resets played for next turn
			player.played = False
		if len(players) == 1:
			self.collect_pot(players[0])
			return True
		else:
			return False
		

	def collect_pot(self, winner):
		"""
		takes money from all players who bet into the pot
		and gives it to the winner. no solution for ties yet
		"""
		pot = 0
		for player in self.players:
			pot += player.take_bet()

		print("%s has won the round. They win the pot of %i chips." % (winner.name, pot))
		winner.add_chips(pot)

	
	def deal_cards(self, deck):
		for player in self.players:
			card1 = deck.pop()
			card2 = deck.pop()
			player.set_player_cards(card1, card2)

	def remove_cards(self):
		for player in self.players:
			player.remove_cards()

	def setup(self):
		"""
		Sets up the game with chip amounts and players.
		Can be called in between rounds.
		"""
		print("Enter the amount of chips all players will start with.")
		start_chips = input("Starting chips: ")
		self.__start_chips = int(start_chips)

		print("Enter the big blind cost. Little blind will be half of the big blind.")
		big_blind = input("Big Blind: ")
		self.__big_blind = int(big_blind)

		setup = True
		cpu_count = 0
		while setup:
			print("There are currently %i players at the table." % (len(self.players)))
			print("To add a human player, type 0.")
			print("To add a smart CPU player, type 1.")
			print("To add a random CPU player, type 2.")
			print("To end setup, hit ENTER. A minimum of 2 players are required.")
			sinput = input("Add player: ")

			if sinput == "":
				if len(self.players) > 1:
					print("Setup Complete.")
					setup = False
				else:
					print("A minimum of 2 players are required.")
			elif sinput == "0":
				name = input("Enter name: ")
				self.players.append(Player(self.__start_chips, 0, name))
			elif sinput == "1":
				cpu_count += 1
				self.players.append(Player(self.__start_chips, 1, "CPU " + str(cpu_count) + "(Smart)"))
			elif sinput == "2":
				cpu_count += 1
				self.players.append(Player(self.__start_chips, 2, "CPU " + str(cpu_count) + "(Random)"))
			else:
				print("Invalid input.")

	def display_players(self):
		"""
		displays information about all players at the table.
		includes money, current bet, etc.
		"""
		print("The players at the table are: ")
		for player in self.players:
			print("%s - %i chips" % (player.name, player.get_chips()))
		print("--------------------------------------------------")
		
	def display_cards(self):
		#returns a string with all cards currently on the table
		card_string = ""
		for card in self.__cards:
			card_string += str(card)
			card_string += " "
		return card_string

	def hand_eval(self, hand1, hand2, table):
		"""
		determines which hand wins given two hands and the table cards.
		returns true if the first hand beats the second hand.
		otherwise returns false
		"""
		hand1_score = 0
		hand2_score = 0

		for card in hand1:
			for card2 in hand1:
				if card.get_suit() == card2.get_suit():
					hand1_score += 1

		for card in hand2:
			for card2 in hand2:
				if card.get_suit() == card2.get_suit():
					hand2_score += 1


		if hand1_score > hand2_score:
			return True
		else:
			return False