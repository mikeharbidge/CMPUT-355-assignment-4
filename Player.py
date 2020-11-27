from Card import Card
from random import randrange

class Player:
	def __init__(self, start_chips, player_type, player_name):
		#type 0 = human, 1 = Smart CPU, 2 = Random CPU
		self.__type = player_type
		self.name = player_name
		self.__chips = start_chips
		self.__card1 = None
		self.__card2 = None
		self.__bet = 0
		#tracks if player has played this turn
		self.played = False

	def get_bet(self):
		return self.__bet

	def add_bet(self, bet):
		#takes chips and places them on the table
		self.remove_chips(bet)
		self.__bet += bet

	def take_bet(self):
		#resets bet to 0 when round is over. returns bet amt
		bet = self.__bet
		self.__bet = 0
		return bet

	def get_chips(self):
		#CPU can access this of other players
		return self.__chips

	def add_chips(self, chips):
		try:
			assert type(chips) == int , "chip value must be int"
			assert chips > 0, "chip value must be positive"
		except AssertionError as inst:
			raise inst
		except Exception as inst:
			raise inst
		else:
			self.__chips += chips
		
	def remove_chips(self, chips):
		try:
			assert str(chips).isdigit(), "invalid chip value"
			assert chips > 0, "chip value must be positive"
		except AssertionError as inst:
			raise inst
		except Exception as inst:
			raise inst
		else:
			self.__chips -= chips

	def set_player_cards(self,card1, card2):
		self.__card1 = card1
		self.__card2 = card2

	def get_player_cards(self):
		return [self.__card1, self.__card2]

	def remove_cards(self):
		self.__card1 = None
		self.__card2 = None

	def turn(self, table):
		"""
		Turn is called by the table on the player's turn
		Return string represents the players move.
		F = fold, C = check/call R = Raise, with amount
		MUST BE UPPER
		IF CALL RAISE PLAYERS BET
		"""
		return_string = ''

		if self.__type == 0:
			return_string = self.human_input(table)
		else:
			return_string = self.random_cpu(table)

		return return_string

	def human_input(self,table):
		"""
		handles human player inputs for their turn
		fold call or raise
		"""
		print("It is your turn to play, %s" % (self.name))
		print("The current bet is %i chips." % (table.get_bet()))
		print("You have %i chips." % (self.__chips))
		print("Your cards are %s and %s." % (self.__card1,self.__card2))
		if self.__bet < table.get_bet():
			inputting = True
			print("You may fold (F), call (C) or raise (R) if you can afford it.")
			print("To raise type R followed by the amount you want to raise on top of the current bet.")
			print("Example: R100")
			while inputting:
				inputting = False
				move = input("User input: ").upper()
				if move == "C":
					#NEED TO CHECK IF THEY HAVE ENOUGH MONEY
					call_amt = table.get_bet() - self.__bet
					self.add_bet(call_amt)
				elif move[0] == "R":
					call_amt = table.get_bet() - self.__bet
					self.add_bet(call_amt)
					raise_amt = int(move.split("R")[1])
					self.add_bet(raise_amt)
					return move
				elif move == "F":
					#folding is handled by the table
					return move
				else:
					inputting = True
					print("Invalid input.")
		else:
			inputting = True
			print("You may check(C) or raise (R) if you can afford it.")
			print("To raise type R followed by the amount you want to raise on top of the current bet.")
			print("Example: R100")
			while inputting:
				inputting = False
				move = input("User input: ").upper()
				if move == "C":
					return move
				elif move[0] == "R":
					raise_amt = int(move.split("R")[1])
					self.add_bet(raise_amt)
					return move
				else:
					inputting = True
					print("Invalid input.")

		return move

	def random_cpu(self, table):
		"""
		random cpu will always check if there is no raise,
		and if the other player raises, will randomly fold or call.
		"""
		print("%s is playing..." % (self.name))
		if self.__bet < table.get_bet():
			#randomly will call or fold if raised
			if randrange(0,2):
				call_amt = table.get_bet() - self.__bet
				self.add_bet(call_amt)
				print("%s calls." % (self.name))
				return "C"
			else:
				#folding is handled by the table
				print("%s folds." % (self.name))
				return "F"
		else:
			#if given the option to check, random AI will always check
			print("%s checks." % (self.name))
			return "C"
		#if somehow doesnt return anything fold?
		return "F"
		

"""player must:
Handle user inputs if human
Handle decision making if AI
"""