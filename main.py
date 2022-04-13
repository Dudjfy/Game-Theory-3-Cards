import random as r

import numpy as np
import matplotlib.pyplot as plt


class Playable:
	options_normal = ["b", "c", "f"]
	options_on_bet = ["b", "f"]

	def __init__(self, name, initial_balance=1000, betting_amount=1):
		self.name = name
		self.balance = initial_balance
		self.initial_balance = initial_balance
		self.card = None
		self.betting_amount = betting_amount
		self.balance_history = np.empty(0, dtype=int)
		self.options = self.options_normal

	def play(self):
		pass

	def play_opener(self):
		pass

	def play_dealer(self, opener_choice):
		pass

	def play_opener_choice_on_dealer_bet(self, opener_choice):
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

	def reset(self):
		self.balance = self.initial_balance
		self.card = None
		self.balance_history = np.empty(1)

	def record_balance_change(self):
		self.balance_history = np.append(self.balance_history, self.balance)


class Player(Playable):
	def __init__(self, name, balance_start=100, print_help=True):
		super().__init__(name, balance_start)
		self.print_help = print_help

	def play(self):
		while True:
			print(self.card)
			if self.print_help:
				print("b - bet (or call), c - check, f - fold")
			inp = input(">>>").strip().lower()
			if inp in self.options:
				return inp
			else:
				print("Invalid command!")

	def play_opener(self):
		self.options = self.options_normal
		self.play()

	def play_dealer(self, opener_choice):
		self.options = self.options_normal
		if opener_choice == "b":
			self.options = self.options_on_bet
		self.play()

	def play_opener_choice_on_dealer_bet(self, dealer_choice):
		self.options = self.options_on_bet
		self.play()

	def reset(self):
		self.balance = self.initial_balance
		self.card = None
		self.options = self.options_normal


class SimpleAI(Playable):
	def play_opener(self):
		if self.card.value == 1:
			return "c"
		elif self.card.value == 2:
			return "c"
		elif self.card.value == 3:
			return "b"

	def play_dealer(self, opener_choice):
		if self.card.value == 1:
			return "f"
		elif self.card.value == 2:
			if opener_choice == "c":
				return "c"
			elif opener_choice == "b":
				return "f"
		elif self.card.value == 3:
			return "b"

	def play_opener_choice_on_dealer_bet(self, opener_choice):
		if self.card.value == 1:
			return "f"
		elif self.card.value == 2:
			return "f"
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
		self.opener_choice = None
		self.dealer_choice = None

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

	def reset_values(self):
		self.pool = 0
		self.opener = None
		self.dealer = None
		self.opener_choice = None
		self.dealer_choice = None

	def initial_setup(self, game):
		self.reset_values()
		self.players_bets()

		self.print_info("Pool: ", self.pool)

		self.choose_opener_and_dealer(game)
		self.choose_cards()

	def player_choices(self):
		self.opener_choice = self.opener.play_opener()
		self.dealer_choice = self.dealer.play_dealer(self.opener_choice)

		if self.opener_choice == "c" and self.dealer_choice == "b":
			self.opener_choice = self.opener.play_opener_choice_on_dealer_bet(self.dealer_choice)

	def check_folds(self):
		if self.opener_choice == "f":
			self.pay_winner(self.dealer,  message_beginning="won", message_end=f", {self.opener.name} folded")
			return False
		if self.dealer_choice == "f":
			self.pay_winner(self.opener, message_beginning="won", message_end=f", {self.dealer.name} folded")
			return False
		return True

	def pay_winner(self, winner, message_beginning="", message_end="", print_outcome=True):
		winner.win(self.pool)

		self.record_balance_changes()

		if print_outcome:
			print(f"{winner.name} {message_beginning} {self.pool}{message_end}")

	def payout(self):
		if not self.check_folds():
			return

		winner = self.dealer
		if self.opener.card.value > self.dealer.card.value:
			winner = self.opener

		self.pay_winner(winner, message_beginning="got the larger card, won")

	def print_final_outcome(self):
		self.print_info("Final", "")
		print()

	def play_game(self, game):
		self.initial_setup(game)

		self.player_choices()

		self.payout()

		self.print_final_outcome()

	def play_games(self):
		for game in range(self.games):
			if not self.check_balance():
				break
			self.play_game(game)

	def print_results(self):
		for p in self.players:
			# print(p.balance_history)
			plt.plot(p.balance_history)
		plt.show()

	def record_balance_changes(self):
		for p in self.players:
			p.record_balance_change()


g = Game(SimpleAI("AI 1"), SimpleAI("AI 2"), games=1000)
g.play_games()
g.print_results()
