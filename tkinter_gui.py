from tkinter import *
from tkinter import ttk

from data_structures import SimpleAiData
from game import Game
from playable import RandomAI, Player


class RelPos:
    def __init__(self, x=0.5, y=0.5):
        self.x = x
        self.y = y


class Size:
    def __init__(self, x=100, y=100):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}x{self.y}"


class Widget:
    def __init__(self, widget, pos, rel_pos):
        self.widget = widget
        self.pos = pos
        self.rel_pos = rel_pos


class TkinterGUI:
    def __init__(self, size=Size(800, 600)):
        self.root = Tk()
        self.root.title("Game Theory: One Card Poker")
        self.og_size = size
        self.size = size
        self.root.geometry(str(self.size))
        self.root.option_add("*font", "arial 14")

        self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.pad = Size(5, 5)
        self.margin = Size(5, 10)

        self.game = Game(RandomAI("Random AI 1"), RandomAI("Random AI 2"))
        self.game_settings = game_settings
        # self.game = Game(Player("P1"), Player("P2"))
        # self.game.set_display_text(True)

        self.main_frame = MainFrame(self.root, self.game, self.size, self.pad, self.margin)

    def start(self, load_main_frame=True):
        if load_main_frame:
            self.load_main_frame()

        self.root.mainloop()

    def load_main_frame(self):
        self.main_frame.load()


class MainFrame:
    player_options = ["Simple AI", "Bluffing AI", "Human"]

    def __init__(self, root, game, size, pad, margin):
        self.root = root
        self.og_size = size
        self.size = self.og_size
        self.main_frame = Frame(root, width=self.size.x, height=self.size.y)
        self.pad = pad
        self.margin = margin

        root.bind("<Return>", lambda event: self.focus_out(event))
        root.bind("<Escape>", lambda event: self.focus_out(event))

        self.games = IntVar(self.main_frame, value=1)
        self.game = game

        self.widgets = []
        self.add_widgets()

    def settings(self):
        print("settings")

    def run(self):
        self.game.set_games(self.games.get())
        self.game.play_games()

    def load(self):
        self.main_frame.pack(fill="both", expand=1)

        # self.load_widgets_grid()
        self.load_widgets_place()

    def load_widgets_grid(self):
        for widget in self.widgets:
            widget.widget.grid(row=widget.pos.x, column=widget.pos.y,
                               padx=self.margin.x, pady=self.margin.y, ipadx=self.pad.x, ipady=self.pad.y)

        col_count, row_count = self.main_frame.grid_size()

        for col in range(col_count):
            self.main_frame.columnconfigure(col, weight=1)

    def load_widgets_place(self):
        for widget in self.widgets:
            widget.widget.place(relx=widget.rel_pos.x, rely=widget.rel_pos.y, anchor=W)

    def focus_out(self, event, games=None):
        self.main_frame.focus_set()
        # print(games)

    def add_widgets(self):
        self.add_first_row()
        self.add_second_row()
        self.add_third_row()
        self.add_fourth_row()

    def add_first_row(self):
        self.games_label_text = "Amount of games simulated:"
        self.games_label = Widget(Label(self.main_frame, text=self.games_label_text),
                                  Size(0, 0), rel_pos=RelPos(0.1, 0.15))
        self.widgets.append(self.games_label)

        self.games_entry = Widget(Entry(self.main_frame, width=20, textvariable=self.games),
                                  Size(0, 1), rel_pos=RelPos(0.42, 0.15))
        self.widgets.append(self.games_entry)

        # self.test_label = Widget(Label(self.main_frame, textvariable=self.games),
        #                          Size(0, 2), rel_pos=RelPos(0.71, 0.15))
        # self.widgets.append(self.test_label)

        self.settings_game_button = Widget(Button(self.main_frame, text="Game Settings", command=self.settings),
                                           pos=Size(1, 1), rel_pos=RelPos(0.72, 0.15))
        self.widgets.append(self.settings_game_button)

    def add_second_row(self):
        self.player_1 = StringVar(self.main_frame, value="Simple AI")
        self.player_1_option_menu = Widget(OptionMenu(self.main_frame, self.player_1, *self.player_options),
                                           pos=Size(1, 0), rel_pos=RelPos(0.13, 0.3))
        self.widgets.append(self.player_1_option_menu)

        self.settings_player_1_button = Widget(Button(self.main_frame, text="Settings", command=self.settings),
                                               pos=Size(1, 1), rel_pos=RelPos(0.31, 0.3))
        self.widgets.append(self.settings_player_1_button)

        self.vs_label = Widget(Label(self.main_frame, text="VS"),
                               Size(1, 1), rel_pos=RelPos(0.49, 0.3))
        self.widgets.append(self.vs_label)

        self.player_2 = StringVar(self.main_frame, value="Simple AI")
        self.player_2_option_menu = Widget(OptionMenu(self.main_frame, self.player_2, *self.player_options),
                                           pos=Size(1, 2), rel_pos=RelPos(0.59, 0.3))
        self.widgets.append(self.player_2_option_menu)

        self.settings_player_2_button = Widget(Button(self.main_frame, text="Settings", command=self.settings),
                                               pos=Size(1, 1), rel_pos=RelPos(0.77, 0.3))
        self.widgets.append(self.settings_player_2_button)

    def add_third_row(self):
        self.run = Widget(Button(self.main_frame, text="Run", bg="green", command=self.run, width=14, height=3),
                          pos=Size(2, 1), rel_pos=RelPos(0.42, 0.5))
        self.widgets.append(self.run)

    def add_fourth_row(self):
        self.progress_bar = Widget(ttk.Progressbar(self.main_frame, orient=HORIZONTAL, length=400, mode="determinate"),
                                   pos=Size(3, 1), rel_pos=RelPos(0.27, 0.8))
        self.widgets.append(self.progress_bar)
