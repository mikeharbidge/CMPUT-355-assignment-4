class Card:
	"""Adapted from a previous project also using cards.
	Written solely by Michael Harbidge for the CMPUT 175 Casino war project."""

	rank_list = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
	suit_list = ["H","C","D","S"]
	def __init__(self, rank, suit):
		try:
			assert str(rank).upper() in Card.rank_list, "Invalid Rank"
			assert suit.upper() in Card.suit_list, "Invalid Suit"
		except AssertionError as inst:
			raise inst
		else:
			self.__rank = str(rank).upper()
			self.__suit = suit.upper()
		
	def get(self):
		return str(self)
	
	def get_rank(self):
		return self.__rank
	
	def get_suit(self):
		return self.__suit
	
	def convert_rank(self,rank):
		return Card.rank_list.index(rank)+2
	
	def __gt__(self, other):
		return Card.rank_list.index(self.get_rank())+2 > other
		
	def __lt__(self, other):
		return Card.rank_list.index(self.get_rank())+2 < other
	
	def __eq__(self, other):
		return Card.rank_list.index(self.get_rank())+2 == other
	
	def __str__(self):
		return "%s%s" % (str(self.__rank),self.__suit)
	def __repr__(self):
		return str(self)