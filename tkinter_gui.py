import time
from tkinter import *
from tkinter import ttk

from data_structures import SimpleAIData, GameSettings
from game import Game
from playable import RandomAI, Player, SimpleAI, BluffingAI
from colorama import Fore, Back, Style


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


class VariableStorage:
    def __init__(self, names, variable):
        self.variable = variable
        self.names = names


class TkinterGUI:
    player_settings_options = ["player_1_settings_frame", "player_2_settings_frame"]

    def __init__(self, size=Size(800, 600)):
        self.root = Tk()
        self.root.title("Game Theory: One Card Poker")
        self.og_size = size
        self.player_settings_size = Size(1660, 830)
        self.size = size
        self.root.geometry(str(self.size))
        # self.root.resizable(False, False)
        self.root.option_add("*font", "arial 14")

        self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.pad = Size(5, 5)
        self.margin = Size(5, 10)

        self.game = Game(SimpleAI("Simple AI 1", text_color=Fore.RED),
                         BluffingAI("Bluffing AI 2", text_color=Fore.BLUE))
        self.game.set_display_text(True)

        self.main_frame = MainFrame(self, self.root, self.size, self.pad, self.margin, self.game)
        self.game_settings_frame = GameSettingsFrame(self, self.root, self.size, self.pad, self.margin)
        self.player_1_settings_frame = PlayerSettingsFrame(self, self.root, self.size, self.pad, self.margin,
                                                           self.game.p1)
        self.player_2_settings_frame = PlayerSettingsFrame(self, self.root, self.size, self.pad, self.margin,
                                                           self.game.p2)
        self.news_searcher_frame = NewsSearcherFrame(self, self.root, self.size, self.pad, self.margin)

        self.frames = {
            "main": self.main_frame,
            "game_settings": self.game_settings_frame,
            "player_1_settings_frame": self.player_1_settings_frame,
            "player_2_settings_frame": self.player_2_settings_frame,
            "news_searcher": self.news_searcher_frame
        }

    def start(self, load_main_frame=True):
        if load_main_frame:
            self.main_frame.load()

        self.root.mainloop()

    def unload_frames(self):
        for frame in self.frames.values():
            frame.frame.pack_forget()

    def load_frame_by_name(self, name):
        if name in self.frames:
            self.root.geometry(str(self.og_size))
            if name in self.player_settings_options:
                self.root.geometry(str(self.player_settings_size))

            self.unload_frames()
            self.frames[name].load()


class FrameBase:
    def __init__(self, parent, root, size, pad, margin):
        self.parent = parent
        self.root = root
        self.og_size = size
        self.size = self.og_size
        self.frame = Frame(self.root, width=self.size.x, height=self.size.y)
        self.pad = pad
        self.margin = margin

        root.bind("<Return>", lambda event: self.focus_out(event))
        root.bind("<Escape>", lambda event: self.focus_out(event))

        self.widgets = []

    def load(self):
        self.frame.pack(fill="both", expand=1)

        self.load_widgets_grid()

    def load_widgets_grid(self):
        for widget in self.widgets:
            widget.widget.grid(row=widget.pos.y, column=widget.pos.x,
                               padx=self.margin.x, pady=self.margin.y, ipadx=self.pad.x, ipady=self.pad.y)

    def load_widgets_place(self):
        for widget in self.widgets:
            widget.widget.place(relx=widget.rel_pos.x, rely=widget.rel_pos.y, anchor=W)

    def focus_out(self, event):
        self.frame.focus_set()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()


class MainFrame(FrameBase):
    player_options = ["Random AI", "Simple AI", "Bluffing AI", "Human"]
    players_with_data = ["Simple AI", "Bluffing AI"]

    def __init__(self, parent, root, size, pad, margin, game):
        super().__init__(parent, root, size, pad, margin)

        self.games = IntVar(self.frame, value=100000)
        self.game = game

        self.add_widgets()

    def settings(self, frame_name, player):
        if isinstance(player, SimpleAI) or isinstance(player, BluffingAI):
            self.parent.load_frame_by_name(frame_name)

    def run(self):
        self.game.set_games(self.games.get())
        self.time_elapsed.set("")

        variables = self.parent.game_settings_frame.variables
        p1, p2 = self.parent.player_1_settings_frame.player, self.parent.player_2_settings_frame.player

        self.game.display_text = variables["display_text"].get()
        self.game.create_log = variables["create_log"].get()
        self.game.use_game_separators = variables["use_game_separator"].get()
        self.game.same_opener_and_dealer = variables["same_opener_and_dealer"].get()
        self.game.set_player(p1, p2)

        self.game.play_games(variables["print_elapsed_time"].get(),
                             variables["print_portions"].get(),
                             variables["print_progress"].get(),
                             lambda percentage: self.update_progress_bar(percentage),
                             lambda time_elapsed: self.change_time_elapsed(time_elapsed))

        if variables["display_matplotlib_results"].get():
            self.game.display_matplotlib_results()

    def load(self):
        self.frame.pack(fill="both", expand=1)

        self.load_widgets_place()

    def add_widgets(self):
        self.add_first_row()
        self.add_second_row()
        self.add_third_row()
        self.add_fourth_row()
        self.add_fifth_row()
        self.add_sixth_row()
        self.add_seventh_row()

    def add_first_row(self):
        self.games_label_text = "Amount of games simulated:"
        self.games_label = Widget(Label(self.frame, text=self.games_label_text),
                                  Size(0, 0), rel_pos=RelPos(0.1, 0.15))
        self.widgets.append(self.games_label)

        self.games_entry = Widget(Entry(self.frame, width=20, textvariable=self.games),
                                  Size(0, 1), rel_pos=RelPos(0.42, 0.15))
        self.widgets.append(self.games_entry)

        self.settings_game_button = Widget(Button(self.frame, text="Game Settings",
                                                  command=lambda: self.parent.load_frame_by_name("game_settings")),
                                           pos=Size(1, 1), rel_pos=RelPos(0.72, 0.15))
        self.widgets.append(self.settings_game_button)

    def add_second_row(self):
        self.player_1 = StringVar(self.frame, value="Simple AI")
        self.player_1.trace("w", self.options_menu_activated_1)
        self.player_1_option_menu = Widget(OptionMenu(self.frame, self.player_1, *self.player_options),
                                           pos=Size(1, 0), rel_pos=RelPos(0.13, 0.3))
        self.widgets.append(self.player_1_option_menu)

        self.settings_player_1_button = Widget(Button(self.frame, text="Settings",
                                                      command=lambda: self.settings("player_1_settings_frame",
                                                                                    self.parent.player_1_settings_frame.player), state=NORMAL),
                                               pos=Size(1, 1), rel_pos=RelPos(0.31, 0.3))
        self.widgets.append(self.settings_player_1_button)

        self.vs_label = Widget(Label(self.frame, text="VS"),
                               Size(1, 1), rel_pos=RelPos(0.49, 0.3))
        self.widgets.append(self.vs_label)

        self.player_2 = StringVar(self.frame, value="Bluffing AI")
        self.player_2.trace("w", self.options_menu_activated_2)
        self.player_2_option_menu = Widget(OptionMenu(self.frame, self.player_2, *self.player_options),
                                           pos=Size(1, 2), rel_pos=RelPos(0.59, 0.3))
        self.widgets.append(self.player_2_option_menu)

        self.settings_player_2_button = Widget(Button(self.frame, text="Settings",
                                                      command=lambda: self.settings("player_2_settings_frame",
                                                                                    self.parent.player_2_settings_frame.player), state=NORMAL),
                                               pos=Size(1, 1), rel_pos=RelPos(0.77, 0.3))
        self.widgets.append(self.settings_player_2_button)

    def add_third_row(self):
        self.run = Widget(Button(self.frame, text="Run", bg="green", command=self.run, width=14, height=3),
                          pos=Size(2, 1), rel_pos=RelPos(0.42, 0.5))
        self.widgets.append(self.run)

    def add_fourth_row(self):
        self.stop = Widget(Button(self.frame, text="Stop", command=self.stop, width=6, height=1),
                          pos=Size(2, 1), rel_pos=RelPos(0.475, 0.62))
        self.widgets.append(self.stop)

    def add_fifth_row(self):
        self.progress_bar = Widget(ttk.Progressbar(self.frame, orient=HORIZONTAL, length=400, mode="determinate"),
                                   pos=Size(3, 1), rel_pos=RelPos(0.27, 0.80))
        self.widgets.append(self.progress_bar)

    def add_sixth_row(self):
        self.time_elapsed = StringVar(self.frame, value="")
        self.time_elapsed_label = Widget(Label(self.frame, textvariable=self.time_elapsed),
                                   pos=Size(3, 1), rel_pos=RelPos(0.49, 0.75))
        self.widgets.append(self.time_elapsed_label)

    def add_seventh_row(self):
        self.news_searcher_button = Widget(Button(self.frame, text="News Searcher",
                                                      command=lambda: self.parent.load_frame_by_name("news_searcher")),
                                               pos=Size(1, 1), rel_pos=RelPos(0.43, 0.92))
        self.widgets.append(self.news_searcher_button)

    def update_progress_bar(self, percentage):
        self.root.update()
        self.progress_bar.widget["value"] = percentage

    def stop(self):
        self.game.break_loop = True

    def change_time_elapsed(self, time_elapsed):
        self.time_elapsed.set(f"{time_elapsed}s")

    def options_menu_activated_1(self, *args):
        self.parent.player_1_settings_frame.change_player(self.player_1.get(), "p1")
        self.settings_player_1_button.widget["state"] = DISABLED
        if self.player_1.get() in self.players_with_data:
            self.settings_player_1_button.widget["state"] = NORMAL

    def options_menu_activated_2(self, *args):
        self.parent.player_2_settings_frame.change_player(self.player_2.get(), "p2")
        self.settings_player_2_button.widget["state"] = DISABLED
        if self.player_2.get() in self.players_with_data:
            self.settings_player_2_button.widget["state"] = NORMAL


class NonMainFrame(FrameBase):
    def __init__(self, parent, root, size, pad, margin):
        super().__init__(parent, root, size, pad, margin)

        self.create_main_frame_button()

    def create_main_frame_button(self):
        self.return_to_main_frame_button = Widget(Button(self.frame, text="Main",
                                                         command=self.return_to_main),
                                                  pos=Size(0, 0), rel_pos=RelPos(0.02, 0.05))
        self.widgets.append(self.return_to_main_frame_button)

    def return_to_main(self):
        self.parent.load_frame_by_name("main")


class PlayerSettingsFrame(NonMainFrame):
    p1_options = {
        "Random AI": RandomAI("Random AI 1", text_color=Fore.RED),
        "Simple AI": SimpleAI("Simple AI 1", data_path="simple_ai_data_1.txt", text_color=Fore.RED),
        "Bluffing AI": BluffingAI("Bluffing AI 1", data_path="bluffing_ai_data_1.txt", text_color=Fore.RED),
        "Human": Player("Player 1", text_color=Fore.RED),
    }
    p2_options = {
        "Random AI": RandomAI("Random AI 2", text_color=Fore.BLUE),
        "Simple AI": SimpleAI("Simple AI 2", data_path="simple_ai_data_2.txt", text_color=Fore.BLUE),
        "Bluffing AI": BluffingAI("Bluffing AI 2", data_path="bluffing_ai_data_2.txt", text_color=Fore.BLUE),
        "Human": Player("Player 2", text_color=Fore.BLUE),
    }

    def __init__(self, parent, root, size, pad, margin, player):
        super().__init__(parent, root, size, pad, margin)
        self.player = player
        self.structured_data = None
        self.construct_data()

        self.variables = []

        if self.structured_data is not None:
            self.create_layout_from_data()

        self.create_save_widgets()

        self.load_widgets_grid()

    def return_to_main(self):
        self.save_data(change_label=False)
        self.saved_label.widget["text"] = ""
        self.parent.load_frame_by_name("main")

    def create_data_widget(self, setting_data, names, x=0, y=0):
        self.variables.append(VariableStorage(names, DoubleVar(value=setting_data)))
        field = Widget(Entry(self.frame, width=4, textvariable=self.variables[-1].variable),
                       Size(x, y), rel_pos=RelPos())
        self.widgets.append(field)

    def create_layout_from_data(self, show_values_in_labels=False):
        self.create_main_frame_button()
        self.create_save_widgets()

        self.variables = []

        y = 1
        x = 1
        for name, element in self.structured_data.data.items():
            label = Widget(Label(self.frame, text=name),
                           Size(x, y), rel_pos=RelPos())
            self.widgets.append(label)

            y += 1
            if x > 1:
                for name2, element2 in element.items():
                    label = Widget(Label(self.frame, text=name2),
                                   Size(x, y), rel_pos=RelPos())
                    self.widgets.append(label)

                    y += 1
                    for name3, element3 in element2.items():
                        label = Widget(Label(self.frame, text=name3),
                                       Size(x, y), rel_pos=RelPos())
                        self.widgets.append(label)

                        y += 1
                        for name4, element4 in element3.items():
                            label = Widget(Label(self.frame, text=name4),
                                           Size(x, y), rel_pos=RelPos())
                            self.widgets.append(label)

                            names = [name, name2, name3, name4]
                            setting_data = self.structured_data.get_dict_element_by_keys_looping(names)
                            self.create_data_widget(setting_data, names, x + 1, y)

                            y += 1

                    x += 2
                    y = 2
            else:
                for name2, element2 in element.items():
                    label = Widget(Label(self.frame, text=name2),
                                   Size(x, y), rel_pos=RelPos())
                    self.widgets.append(label)

                    y += 1
                    for name3, element3 in element2.items():
                        label = Widget(Label(self.frame, text=name3),
                                       Size(x, y), rel_pos=RelPos())
                        self.widgets.append(label)

                        names = [name, name2, name3]
                        setting_data = self.structured_data.get_dict_element_by_keys_looping(names)
                        self.create_data_widget(setting_data, names, x + 1, y)

                        y += 1
                x += 2
            y = 1

    def save_data(self, change_label=True):
        for var_storage in self.variables:
            self.structured_data.set_element_by_keys(var_storage.names, var_storage.variable.get())
        self.structured_data.save()

        if change_label:
            self.saved_label.widget["text"] = "Saved!"
            self.saved_label.widget["fg"] = "green"
            self.root.update()
            self.root.after(500)
            self.saved_label.widget["fg"] = "black"

    def change_player(self, player, player_list):
        self.player = self.p1_options[player] if player_list == "p1" else self.p2_options[player]
        # print(self.player)
        self.construct_data()

    def construct_data(self):
        if isinstance(self.player, Player) or isinstance(self.player, RandomAI):
            self.structured_data = None
        elif isinstance(self.player, SimpleAI) or isinstance(self.player, BluffingAI):
            self.structured_data = self.player.structured_data
            self.frame = Frame(self.root, width=self.size.x, height=self.size.y)
            self.create_layout_from_data()

    def create_save_widgets(self):
        self.save_button = Widget(Button(self.frame, text="Save",
                                         command=self.save_data),
                                  pos=Size(13, 13), rel_pos=RelPos(0.02, 0.05))
        self.widgets.append(self.save_button)
        self.saved_label = Widget(Label(self.frame, text=""),
                                  pos=Size(13, 12), rel_pos=RelPos(0.02, 0.05))
        self.widgets.append(self.saved_label)


class GameSettingsFrame(NonMainFrame):
    def __init__(self, parent, root, size, pad, margin):
        super().__init__(parent, root, size, pad, margin)
        self.structured_data = GameSettings()
        self.variables = dict()

        self.create_layout_from_data()

        self.save_button = Widget(Button(self.frame, text="Save",
                                         command=self.save_data),
                                  pos=Size(4, 8), rel_pos=RelPos(0.02, 0.05))
        self.widgets.append(self.save_button)
        self.saved_label = Widget(Label(self.frame, text=""),
                                  pos=Size(5, 8), rel_pos=RelPos(0.02, 0.05))
        self.widgets.append(self.saved_label)

        self.load_widgets_grid()

    def return_to_main(self):
        self.save_data(change_label=False)
        self.saved_label.widget["text"] = ""
        self.parent.load_frame_by_name("main")

    def create_data_widget(self, setting_data, name, y, variable_type, widget_type, show_values_in_labels=False):
        self.variables[name] = variable_type(name=name, value=setting_data)
        if isinstance(setting_data, bool):
            field = Widget(widget_type(self.frame, width=1, height=1, variable=self.variables[name]),
                           Size(2, y + 1), rel_pos=RelPos(0.42, 0.15))
        else:
            field = Widget(widget_type(self.frame, width=20, textvariable=self.variables[name]),
                           Size(2, y + 1), rel_pos=RelPos(0.42, 0.15))
        self.widgets.append(field)

        if show_values_in_labels:
            label = Widget(Label(self.frame, textvariable=self.variables[name]),
                           Size(3, y + 1), rel_pos=RelPos())
            self.widgets.append(label)

    def create_layout_from_data(self, show_values_in_labels=False):
        for y, name in enumerate(self.structured_data.data):
            label = Widget(Label(self.frame, text=name),
                           Size(1, y + 1), rel_pos=RelPos())
            self.widgets.append(label)

            setting_data = self.structured_data.data[name]
            if isinstance(setting_data, float):
                self.create_data_widget(setting_data, name, y, DoubleVar, Entry, show_values_in_labels)
            elif isinstance(setting_data, bool):
                self.create_data_widget(setting_data, name, y, BooleanVar, Checkbutton, show_values_in_labels)
            elif isinstance(setting_data, int):
                self.create_data_widget(setting_data, name, y, IntVar, Entry, show_values_in_labels)

    def save_data(self, change_label=True):
        for name, variable in self.variables.items():
            self.structured_data.set_element_by_keys([name], variable.get())
        self.structured_data.save()

        if change_label:
            self.saved_label.widget["text"] = "Saved!"
            self.saved_label.widget["fg"] = "green"
            self.root.update()
            self.root.after(500)
            self.saved_label.widget["fg"] = "black"


class NewsSearcherFrame(NonMainFrame):
    def __init__(self, parent, root, size, pad, margin):
        super().__init__(parent, root, size, pad, margin)

        self.create_main_frame_button()

    def create_main_frame_button(self):
        self.return_to_main_frame_button = Widget(Button(self.frame, text="Main",
                                                         command=self.return_to_main),
                                                  pos=Size(0, 0), rel_pos=RelPos(0.02, 0.05))
        self.widgets.append(self.return_to_main_frame_button)

    def return_to_main(self):
        self.parent.load_frame_by_name("main")
