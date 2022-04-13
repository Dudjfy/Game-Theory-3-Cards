import random as r


class Playable:
	options = ["b", "c", "f"]

	def __init__(self, name, balance_start=100, betting_amount=1):
		self.name = name
		self.balance = balance_start
		self.card = None
		self.betting_amount = betting_amount

	def play(self):
		pass

	def play_opener(self):
		pass

	def play_dealer(self):
		pass

	def check_balance(self):
		return self.balance - self.betting_amount >= 0

	def bet(self):
		if self.check_balance():
			self.balance -= self.betting_amount
			return self.betting_amount
		return 0

	def win(self, amount):
		self.balance += amount

	def set_card(self, card):
		self.card = card


class Player(Playable):
	def __init__(self, name, balance_start=100, print_help=True):
		super().__init__(name, balance_start)
		self.print_help = print_help

	def play(self):
		print(self.card)
		if self.print_help:
			print("b - bet (or call), c - check, f - fold")
		inp = input(">>>").strip().lower()
		if inp in self.options:
			return inp

	def play_opener(self):
		self.play()

	def play_dealer(self):
		self.play()


class SimpleAI(Playable):
	def play_opener(self):
		if self.card.value == 1:
			return "f"
		elif self.card.value == 2:
			return "f"
		elif self.card.value == 3:
			return "b"

	def play_dealer(self):
		if self.card.value == 1:
			return "c"
		elif self.card.value == 2:
			return "c"
		elif self.card.value == 3:
			return "b"


class Card:
	def __init__(self, value: int):
		self.value = value
		self.face_up = True

	def __str__(self):
		return f"[{self.value:}]" if self.face_up else "[■]"

	def flip_face(self):
		self.face_up = not self.face_up


class Game:
	def __init__(self, p1, p2, games=1):
		self.games = games
		self.score_p1 = 0
		self.score_p2 = 0
		self.cards = [Card(1), Card(2), Card(3)]
		self.p1 = p1
		self.p2 = p2
		self.players = [self.p1, self.p2]

		self.pool = 0
		self.opener = None
		self.dealer = None

	def check_balance(self):
		return all([p.check_balance() for p in self.players])

	def players_bets(self):
		for p in self.players:
			self.pool += p.bet()

		return self.pool

	def choose_opener_and_dealer(self, i, print_outcome=True):
		self.opener = self.p1 if i % 2 == 0 else self.p2
		self.dealer = self.p2 if i % 2 == 0 else self.p1

		if print_outcome:
			print(f"Opener: {self.opener.name}, Dealer: {self.dealer.name}")

	def print_info(self, info_name, info_data):
		print(f"{info_name}{info_data} - {self.p1.name}: {self.p1.balance}, {self.p2.name}: {self.p2.balance}")

	def choose_cards(self, print_outcome=True):
		self.p1.card, self.p2.card = r.sample(self.cards, k=2)

		if print_outcome:
			for p in self.players:
				print(f"{p.name} {p.card}")

	def initial_setup(self, game):
		self.pool = 0
		self.players_bets()

		self.print_info("Pool: ", self.pool)

		self.choose_opener_and_dealer(game)
		self.choose_cards()

	def play_game(self, game):
		self.initial_setup(game)

		if not self.opener.play():
			self.dealer.win(self.pool)
			print(f"{self.opener.name} folded, {self.dealer.name} won {self.pool}")
			print(f"Final - {self.p1.name}: {self.p1.balance}, {self.p2.name}: {self.p2.balance}")
			print(" ")
			continue

		temp_bet = self.opener.bet()
		if temp_bet > 0:
			self.pool += temp_bet
		else:
			print(f"{self.opener.name} out of balance :(")
			break

		if not self.dealer.play():
			self.opener.win(self.pool)

			print(f"{self.dealer.name} folded, {self.opener.name} won {self.pool}")
			print(f"Final - {self.p1.name}: {self.p1.balance}, {self.p2.name}: {self.p2.balance}")
			print(" ")
			continue

		temp_bet = self.dealer.bet()
		if temp_bet > 0:
			self.pool += temp_bet
		else:
			print(f"{self.dealer.name} out of balance :(")
			break

		if self.opener.card.value > self.dealer.card.value:
			self.opener.win(self.pool)
			print(f"{self.dealer.name} got the larger card, won {self.pool}")
		else:
			print(f"{self.opener.name} got the larger card, won {self.pool}")

			self.dealer.win(self.pool)

		print(f"Final - {self.p1.name}: {self.p1.balance}, {self.p2.name}: {self.p2.balance}")
		print(" ")

	def play_games(self):
		for game in range(self.games):
			if not self.check_balance():
				break
			self.play_game(game)



g = Game(SimpleAI("AI 1"), SimpleAI("AI 2"), games=100)
g.play_games()