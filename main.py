import random as r


class Playable:
	def __init__(self, name, money_start=100):
		self.name = name
		self.money = money_start
		self.card = None
	
	def play(self):
		pass
		
	def bet(self, amount=1):
		if self.money - amount >= 0:
			self.money -= amount
			return amount
		return 0
	
	def win(self, amount):
		self.money += amount
	
	def set_card(self, card):
		self.card = card
	
	
class Player(Playable):
	def play(self):
		print(self.card)
		print("f - fold, c - call")
		# inp = input(">>>").strip().lower()
		
		return inp == "c"
		

class SimpleAI(Playable):
	def __init__(self, name, money_start=100, bluff_chance=0.5, call_bluff_chance=0.5):
		self.name = name
		self.money = money_start
		self.card = None
		self.bluff = bluff_chance
		self.cbluff = call_bluff_chance
	
	def play(self):
		if self.card.value == 1:
			return False
		elif self.card.value == 2:
			return False
		elif self.card.value == 3:
			return True


class Card:
    def __init__(self, value: int):
        self.value = value
        self.face_up = True

    # returns card's symbol and suit if faced up, otherwise returns card faced down
    def __str__(self):
        return f"[{self.value:}]" if self.face_up else "[■]"

    # Flips cards face
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
	
	def play_games(self):
		for game in range(self.games):
			pool = 0
			for p in self.players:
				pool += p.bet()
			
			print(f"Pool: {pool} - {self.p1.name}: {self.p1.money}, {self.p1.name}: {self.p2.money}")
			
			opener = r.choice(self.players)
			if opener.name == "AI 1":
				dealer = self.p2
			else:
				dealer = self.p1
			print(f"Opener: {opener.name}, Dealer: {dealer.name}")
			
			self.p1.card, self.p2.card = r.sample(self.cards, k=2)
			for p in self.players:
				print(f"{p.name} {p.card}")
			
			if not opener.play():
				dealer.win(pool)
				print(f"{opener.name} folded, {dealer.name} won {pool}")
				print(f"Final - {self.p1.name}: {self.p1.money}, {self.p1.name}: {self.p2.money}")
				print(" ")
				continue
			
			temp_bet = opener.bet()
			if temp_bet > 0:
				pool += temp_bet
			else:
				print(f"{opener.name} out of money :(")
				break
			
			
			if not dealer.play():
				opener.win(pool)
				
				print(f"{dealer.name} folded, {opener.name} won {pool}")
				print(f"Final - {self.p1.name}: {self.p1.money}, {self.p1.name}: {self.p2.money}")
				print(" ")
				continue
			
			temp_bet = dealer.bet()
			if temp_bet > 0:
				pool += temp_bet
			else:
				print(f"{dealer.name} out of money :(")
				break
			
			if opener.card.value > dealer.card.value:
				opener.win(pool)
				print(f"{dealer.name} got the larger card, won {pool}")
			else:
				print(f"{opener.name} got the larger card, won {pool}")
			
				dealer.win(pool)
			
			print(f"Final - {self.p1.name}: {self.p1.money}, {self.p1.name}: {self.p2.money}")
			print(" ")
			
			
g = Game(SimpleAI("AI 1"), SimpleAI("AI 2"), games=100)

g.play_games()