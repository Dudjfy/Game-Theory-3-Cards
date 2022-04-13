from game import Game
from playable import SimpleAI

g = Game(SimpleAI("AI 1"), SimpleAI("AI 2"), games=100000, display_text=False)

g.play_games(print_progress=True, print_portions=100, print_elapsed_time=True)

g.print_results()
