"""One card poker game module"""

import random
import time
import logging
import matplotlib.pyplot as plt
from card import Card


logging.basicConfig(filename="log.log", level=logging.INFO, format="%(message)s", filemode="w")


class Game:
    """Game class for simulating One Card Poker, can be run both in console and with a
    tkinter GUI"""
    def __init__(self, p_1, p_2, games=1, display_text=False, create_log=False,
                 use_game_separators=True,
                 same_opener_and_dealer=False):
        self.break_loop = False
        self.games = games
        self.score_p_1 = 0
        self.score_p_2 = 0
        self.cards = [Card(1), Card(2), Card(3)]
        self.p_1 = p_1
        self.p_2 = p_2
        self.players = [self.p_1, self.p_2]

        self.pool = 0
        self.opener = None
        self.dealer = None
        self.player_folded = False

        self.display_text = display_text
        self.use_game_separators = use_game_separators
        self.create_log = create_log
        self.same_opener_and_dealer = same_opener_and_dealer

    def reset_new_games(self):
        """Resets new games"""
        for player in self.players:
            player.reset()

    def set_player(self, p_1, p_2):
        """Sets the player variables to the input players"""
        self.p_1, self.p_2 = p_1, p_2
        self.players = [self.p_1, self.p_2]

    def set_display_text(self, display_text):
        """Sets display text"""
        self.display_text = display_text

    def set_games(self, games):
        """Sets the amount of games"""
        self.games = games

    def check_balance(self):
        """Checks if there is enough funds for all players and returns if true,
        older system functionality for playing with a fixed amount of money"""
        return all(p.check_balance() for p in self.players)

    def players_bets(self):
        """takes bets from players"""
        for player in self.players:
            self.pool += player.bet()

        return self.pool

    def choose_opener_and_dealer(self, i):
        """Choses opener and dealer based on the preference,  influenced by current
        game index if the option of switching sides (NOT same dealer) is chosen"""
        if not self.same_opener_and_dealer:
            self.opener = self.p_1 if i % 2 == 0 else self.p_2
            self.dealer = self.p_2 if i % 2 == 0 else self.p_1
        else:
            self.opener = self.p_1
            self.dealer = self.p_2

        if self.display_text:
            print(f"Opener: {self.opener.text_color}{self.opener.name}{self.opener.default_color}, "
                  f"Dealer: {self.dealer.text_color}{self.dealer.name}{self.dealer.default_color}")
        if self.create_log:
            logging.info("Opener: %s, "
                         "Dealer: %s", self.opener.name, self.dealer.name)

    def print_info(self, info_name, info_data):
        """Prints/logs info of the current situation"""
        if self.display_text:
            print(f"{info_name}{info_data} - "
                  f"{self.p_1.text_color}{self.p_1.name}{self.p_1.default_color}: "
                  f"{self.p_1.get_balance()}, "
                  f"{self.p_2.text_color}{self.p_2.name}{self.p_2.default_color}: "
                  f"{self.p_2.get_balance()}")
        if self.create_log:
            logging.info("%s%s - %s: %s, %s: %s",
                         info_name, info_data, self.p_1.name, self.p_1.get_balance(),
                         self.p_2.name, self.p_2.get_balance())

    def choose_cards(self):
        """Chooses cards for players, prints/logs it"""
        self.p_1.card, self.p_2.card = random.sample(self.cards, k=2)

        if self.display_text:
            print(f"\t{self.p_1.text_color}{self.p_1.name}{self.p_1.default_color} "
                  f"{self.p_1.card} - "
                  f"{self.p_2.text_color}{self.p_2.name}{self.p_2.default_color} {self.p_2.card}")

        if self.create_log:
            logging.info("\t%s %s - %s %s", self.p_1.name, self.p_1.card, self.p_2.name,
                         self.p_2.card)

    def reset_values(self):
        """Resets values to default"""
        self.pool = 0
        self.opener = None
        self.dealer = None
        self.player_folded = False

    def initial_setup(self, game):
        """Initial setup for simulations"""
        self.reset_values()
        self.players_bets()

        self.print_info("Pool: ", self.pool)

        self.choose_opener_and_dealer(game)
        self.choose_cards()

    def get_opposite_player(self, player):
        """Returns the opposite player to the given one"""
        if player is self.opener:
            return self.dealer
        return self.opener

    def player_choice(self, player, play_method, opponent_choice=None):
        """Players choice based on input from console, least developed mode because hardly used,
        mostly for debugging"""
        player_choice = play_method(opponent_choice)
        if player_choice == "b":
            self.pool += player.bet()
        if self.display_text:
            print(f"\t\t{player.text_color}{player.name}{player.default_color} - {player_choice}")
        if self.create_log:
            logging.info("\t\t%s - %s", player.name, player_choice)
        if player_choice == "f":
            self.player_folded = True
            self.pay_winner(self.get_opposite_player(player),
                            message_beginning="won",
                            message_end=" folded", display_loser_name=True)
        return player_choice

    def player_choices(self):
        """Runs the different choices based on how the game unfolds"""
        opener_choice = self.player_choice(self.opener, self.opener.play_opener)
        if self.player_folded:
            return

        dealer_choice = self.player_choice(self.dealer, self.dealer.play_dealer, opener_choice)
        if self.player_folded:
            return

        if opener_choice == "c" and dealer_choice == "b":
            self.player_choice(self.opener, self.opener.play_opener_choice_on_dealer_bet,
                               dealer_choice)

    def pay_winner(self, winner, message_beginning="", message_end="", display_loser_name=False):
        """Pays the payout to the winner, prints/logs it"""
        winner.win(self.pool)
        loser = self.get_opposite_player(winner)

        self.record_balance_changes()

        if self.display_text:
            if display_loser_name:
                print(f"{winner.text_color}{winner.name}{winner.default_color} {message_beginning} "
                      f"{self.pool}, {loser.text_color}{loser.name}{loser.default_color}"
                      f"{message_end}")
            else:
                print(f"{winner.text_color}{winner.name}{winner.default_color} {message_beginning} "
                      f"{self.pool}{message_end}")
        if self.create_log:
            logging.info("%s %s %s%s%s",
                         winner.name, message_beginning, self.pool,
                         ', ' + loser.name if display_loser_name else '', message_end)

    def payout(self):
        """Checks for folding and pays payouts"""
        if self.player_folded:
            return

        winner = self.dealer
        if self.opener.card.value > self.dealer.card.value:
            winner = self.opener

        self.pay_winner(winner, message_beginning="got the larger card, won")

    def print_final_outcome(self):
        """Prints/logs final outcome"""
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

    def play_game(self, game):
        """Plays a game"""
        self.initial_setup(game)

        self.player_choices()

        self.payout()

        self.print_final_outcome()

    def play_games(self, print_elapsed_time=False, print_portions=1, print_progress=False,
                   increase_progress_method=lambda: None, change_time_elapsed=lambda: None):
        """Plays the specified amount of games, logs time taken etc if specified in parameters"""
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
        """Displays matbloplib results with a interactive graph"""
        plt.clf()
        for player in self.players:
            plt.plot(player.balance_history, label=player.name)
        plt.legend()
        plt.show()

    def record_balance_changes(self):
        """Records balance changes for the further analysis with the graph"""
        for player in self.players:
            player.record_balance_change()
