from game import Game
from playable import SimpleAI, BluffingAI, Player, RandomAI

games = 1000
# ai_1 = SimpleAI("Simple AI", initial_balance=games // 10, use_relative_balance=True)
# ai_2 = SimpleAI("Simple AI", initial_balance=games // 10)
ai_1 = BluffingAI("Bluffing AI", initial_balance=games // 10, use_relative_balance=True)
# ai_1 = Player("Player")
# ai_2 = BluffingAI("Bluffing AI", initial_balance=games // 10, use_relative_balance=True)
# ai_1 = RandomAI("Random AI", initial_balance=games // 10, use_relative_balance=True)
ai_2 = RandomAI("Random AI", initial_balance=games // 10, use_relative_balance=True)
g = Game(ai_1, ai_2, games=games, display_text=False, create_log=True)

g.play_games(print_progress=True, print_portions=100, print_elapsed_time=True)

g.print_results()
