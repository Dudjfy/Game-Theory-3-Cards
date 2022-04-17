from data_structures import GameSettings
from game import Game
from playable import SimpleAI, BluffingAI, Player, RandomAI
from colorama import Fore, Back, Style
from tkinter_gui import TkinterGUI


# games = 100
# # ai_1 = SimpleAI("Simple AI", initial_balance=games // 10, use_relative_balance=True)
# # ai_2 = SimpleAI("Simple AI", initial_balance=games // 10)
# # ai_1 = BluffingAI("Bluffing AI", initial_balance=games // 10, use_relative_balance=True, text_color=Fore.BLUE)
# # ai_1 = Player("Player")
# ai_1 = RandomAI("Random AI", initial_balance=games // 10, use_relative_balance=True, text_color=Fore.BLUE)
# ai_2 = BluffingAI("Bluffing AI", initial_balance=games // 10, use_relative_balance=True, text_color=Fore.RED)
# # ai_2 = RandomAI("Random AI", initial_balance=games // 10, use_relative_balance=True, text_color=Fore.RED)
# g = Game(ai_1, ai_2, games=games, display_text=False, create_log=False)
#
# g.play_games(print_progress=False, print_portions=100, print_elapsed_time=False)
#
# g.display_matplotlib_results()

win = TkinterGUI()
win.start()

# gs = GameSettings()
# gs.reset_to_default_data()
# gs.save()

