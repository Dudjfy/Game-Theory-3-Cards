from line_profiler_pycharm import profile
from card import Card
import matplotlib.pyplot as plt
import random
import time
import logging


logging.basicConfig(filename="log.log", level=logging.INFO, format="%(message)s", filemode="w")


class Game:
    def __init__(self, p1, p2, games=1, display_text=False, create_log=False, use_game_separators=True):
        self.break_loop = False
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
        self.player_folded = False

        self.display_text = display_text
        self.use_game_separators = use_game_separators
        self.create_log = create_log

    def reset_new_games(self):
        for p in self.players:
            p.reset()

    def set_player(self, p1, p2):
        self.p1, self.p2 = p1, p2
        self.players = [self.p1, self.p2]

    def set_display_text(self, display_text):
        self.display_text = display_text

    def set_games(self, games):
        self.games = games

    def check_balance(self):
        return all([p.check_balance() for p in self.players])

    def players_bets(self):
        for p in self.players:
            self.pool += p.bet()

        return self.pool

    def choose_opener_and_dealer(self, i):
        self.opener = self.p1 if i % 2 == 0 else self.p2
        self.dealer = self.p2 if i % 2 == 0 else self.p1

        if self.display_text:
            print(f"Opener: {self.opener.text_color}{self.opener.name}{self.opener.default_color}, "
                  f"Dealer: {self.dealer.text_color}{self.dealer.name}{self.dealer.default_color}")
        if self.create_log:
            logging.info(f"Opener: {self.opener.name}, "
                         f"Dealer: {self.dealer.name}")

    def print_info(self, info_name, info_data):
        if self.display_text:
            print(f"{info_name}{info_data} - "
                  f"{self.p1.text_color}{self.p1.name}{self.p1.default_color}: {self.p1.get_balance()}, "
                  f"{self.p2.text_color}{self.p2.name}{self.p2.default_color}: {self.p2.get_balance()}")
        if self.create_log:
            logging.info(f"{info_name}{info_data} - "
                         f"{self.p1.name}: {self.p1.get_balance()}, "
                         f"{self.p2.name}: {self.p2.get_balance()}")

    @profile
    def choose_cards(self):
        self.p1.card, self.p2.card = random.sample(self.cards, k=2)

        if self.display_text:
            print(f"\t{self.p1.text_color}{self.p1.name}{self.p1.default_color} {self.p1.card} - "
                  f"{self.p2.text_color}{self.p2.name}{self.p2.default_color} {self.p2.card}")

        if self.create_log:
            logging.info(f"\t{self.p1.name} {self.p1.card} - "
                         f"{self.p2.name} {self.p2.card}")

    def reset_values(self):
        self.pool = 0
        self.opener = None
        self.dealer = None
        self.player_folded = False

    @profile
    def initial_setup(self, game):
        self.reset_values()
        self.players_bets()

        self.print_info("Pool: ", self.pool)

        self.choose_opener_and_dealer(game)
        self.choose_cards()

    def get_opposite_player(self, player):
        if player is self.opener:
            return self.dealer
        else:
            return self.opener

    def player_choice(self, player, play_method, opponent_choice=None):
        player_choice = play_method(opponent_choice)
        if player_choice == "b":
            self.pool += player.bet()
        if self.display_text:
            print(f"\t\t{player.text_color}{player.name}{player.default_color} - {player_choice}")
        if self.create_log:
            logging.info(f"\t\t{player.name} - {player_choice}")
        if player_choice == "f":
            self.player_folded = True
            self.pay_winner(self.get_opposite_player(player),
                            message_beginning="won",
                            message_end=f" folded", display_loser_name=True)
        return player_choice

    def player_choices(self):
        opener_choice = self.player_choice(self.opener, self.opener.play_opener)
        if self.player_folded:
            return

        dealer_choice = self.player_choice(self.dealer, self.dealer.play_dealer, opener_choice)
        if self.player_folded:
            return

        if opener_choice == "c" and dealer_choice == "b":
            self.player_choice(self.opener, self.opener.play_opener_choice_on_dealer_bet, dealer_choice)

    def pay_winner(self, winner, message_beginning="", message_end="", display_loser_name=False):
        winner.win(self.pool)
        loser = self.get_opposite_player(winner)

        self.record_balance_changes()

        if self.display_text:
            if display_loser_name:
                print(f"{winner.text_color}{winner.name}{winner.default_color} {message_beginning} "
                      f"{self.pool}, {loser.text_color}{loser.name}{loser.default_color}{message_end}")
            else:
                print(f"{winner.text_color}{winner.name}{winner.default_color} {message_beginning} "
                      f"{self.pool}{message_end}")
        if self.create_log:
            logging.info(f"{winner.name} {message_beginning} "
                         f"{self.pool}{', ' + loser.name if display_loser_name else ''}{message_end}")

    def payout(self):
        if self.player_folded:
            return

        winner = self.dealer
        if self.opener.card.value > self.dealer.card.value:
            winner = self.opener

        self.pay_winner(winner, message_beginning="got the larger card, won")

    def print_final_outcome(self):
        self.print_info("Final", "")
        if self.display_text:
            print()
            if self.use_game_separators:
                print("-" * 50)
                print()
        if self.create_log:
            logging.info("")
            if self.use_game_separators:
                logging.info("-" * 50)
                logging.info("")

    # @profile
    def play_game(self, game):
        self.initial_setup(game)

        self.player_choices()

        self.payout()

        self.print_final_outcome()

    def play_games(self, print_elapsed_time=False, print_portions=1, print_progress=False,
                   increase_progress_method=lambda: None, change_time_elapsed=lambda: None):
        if print_elapsed_time:
            start = time.time()

        if print_progress:
            print_step = self.games // print_portions

        self.reset_new_games()
        self.break_loop = False
        for game in range(self.games):
            if self.break_loop:
                break
            if print_progress:
                if (game + 1) % print_step == 0:
                    percentage = (100 // print_portions) * ((game // print_step) + 1)
                    increase_progress_method(percentage)
                    if print_progress:
                        print(f"{percentage}%")

            if not self.check_balance():
                break
            self.play_game(game)

        if print_elapsed_time:
            end = time.time()
            time_elapsed = round(end - start, 2)
            print(f"{time_elapsed}s")
            change_time_elapsed(time_elapsed)

    def display_matplotlib_results(self):
        for p in self.players:
            plt.plot(p.balance_history, label=p.name)
        plt.legend()
        plt.show()

    def record_balance_changes(self):
        for p in self.players:
            p.record_balance_change()
