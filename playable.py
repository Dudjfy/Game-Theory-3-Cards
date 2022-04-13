import random

import numpy as np

from betting import OpenerBetting, DealerBetting


class Playable:
    options_normal = ["b", "c", "f"]
    options_on_bet = ["b", "f"]

    def __init__(self, name, initial_balance=10000, betting_amount=1):
        self.name = name
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.card = None
        self.betting_amount = betting_amount
        self.balance_history = []
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
        self.balance_history = []

    def record_balance_change(self):
        self.balance_history.append(self.balance)


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


class BluffingAI(Playable):
    def __init__(self, name, initial_balance=10000, betting_amount=1):
        super().__init__(name, initial_balance, betting_amount)
        self.opener_betting = OpenerBetting()
        self.dealer_betting = DealerBetting()

    def play_opener(self):
        rand = random.random()
        if self.card.value == 1:
            return "b" if rand < self.opener_betting.bluff_on_1 else "c"
        elif self.card.value == 2:
            return "b" if rand < self.opener_betting.bluff_on_2 else "c"
        elif self.card.value == 3:
            return "c" if rand < self.opener_betting.bluff_on_3 else "b"

    def play_dealer(self, opener_choice):
        rand = random.random()
        if self.card.value == 1:
            if opener_choice == "c":
                return "b" if rand < self.dealer_betting.bluff_on_1 else "c"
            else:
                return "f"
        elif self.card.value == 2:
            if opener_choice == "c":
                return "c"
            elif opener_choice == "b":
                return "b" if rand < self.dealer_betting.bluff_on_2 else "f"
        elif self.card.value == 3:
            return "b"

    def play_opener_choice_on_dealer_bet(self, opener_choice):
        return self.play_dealer(opener_choice)
