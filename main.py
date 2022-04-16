from game import Game
from playable import SimpleAI, BluffingAI, Player

games = 10000
ai_1 = SimpleAI("Simple AI", initial_balance=games // 10, use_relative_balance=True)
# ai_2 = SimpleAI("Simple AI", initial_balance=games // 10)
# ai_1 = BluffingAI("Bluffing AI", initial_balance=games // 10)
# ai_1 = Player("Player")
ai_2 = BluffingAI("Bluffing AI", initial_balance=games // 10, use_relative_balance=True)
g = Game(ai_1, ai_2, games=games, display_text=False)

g.play_games(print_progress=False, print_portions=100, print_elapsed_time=False)

g.print_results()
