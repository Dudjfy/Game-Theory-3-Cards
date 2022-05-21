"""Data structure classes"""

import json
from os.path import exists


class DataHolder:
    """Generic parent class for data holder with generic methods for data loading, saving,
    extraction etc"""
    default_data = {}

    def __init__(self, path="test.txt"):
        self.data = None
        self.path = path
        self.load()

    def reset_to_default_data(self):
        """Resets current data to default"""
        self.data = self.default_data

    def load(self):
        """Loads data form file path"""
        if exists(self.path):
            with open(self.path, "r", encoding="utf8") as json_file:
                self.data = json.load(json_file)
        else:
            self.data = self.default_data
            self.save()

    def save(self):
        """Saves data to file by path"""
        with open(self.path, "w", encoding="utf8") as json_file:
            json.dump(self.data, json_file, indent=4)

    def print_whole_with_indents(self, indent=4):
        """Prints whole json data with indents"""
        print(json.dumps(self.data, indent=indent))

    def get_dict_element_by_keys_recursively(self, args, msg=None):
        """Returns dict elements by give list och keys recursively"""
        if len(args) <= 0:
            return msg

        if msg is None:
            return self.get_dict_element_by_keys_recursively(args[1:], msg=self.data[args[0]])
        return self.get_dict_element_by_keys_recursively(args[1:], msg=msg[args[0]])

    def get_dict_element_by_keys_looping(self, args):
        """Returns dict elements by give list och keys by looping"""
        msg = self.data
        for arg in args:
            msg = msg[arg]
        return msg

    def print_element_by_keys(self, args):
        """Prints element by given keys"""
        print(self.get_dict_element_by_keys_looping(args))

    def set_element_by_keys(self, args, new_value=None):
        """Sets (inserts) element by keys"""
        data = self.data
        last_key = args[-1]
        for k in args[:-1]:
            data = data[k]
        data[last_key] = new_value


class GameSettings(DataHolder):
    """Game settings data structure holder"""
    default_data = {
        "display_text": False,
        "create_log": False,
        "use_game_separator": True,
        "print_elapsed_time": True,
        "print_portions": 100,
        "print_progress": True,
        "display_matplotlib_results": True,
        "same_opener_and_dealer": True,
    }

    def __init__(self, path="game_settings.txt"):
        super().__init__(path)


class SimpleAIData(DataHolder):
    """Simple AI data structure holder"""
    default_data = {
        "opener_first_move": {
            "one": {
                "f": 0.0,
                "c": 1.0,
                "b": 0.0,
            },
            "two": {
                "f": 0.0,
                "c": 1.0,
                "b": 0.0,
            },
            "three": {
                "f": 0.0,
                "c": 0.0,
                "b": 1.0,
            }
        },
        "dealer_first_move": {
            "one": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 1.0,
                    "b": 0.0,
                },
                "opponent_b": {
                    "f": 1.0,
                    "c": 0.0,
                    "b": 0.0,
                }
            },
            "two": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 1.0,
                    "b": 0.0,
                },
                "opponent_b": {
                    "f": 1.0,
                    "c": 0.0,
                    "b": 0.0,
                }
            },
            "three": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                },
                "opponent_b": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                }
            }
        },
        "opener_second_move": {
            "one": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 1.0,
                    "b": 0.0,
                },
                "opponent_b": {
                    "f": 1.0,
                    "c": 0.0,
                    "b": 0.0,
                }
            },
            "two": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 1.0,
                    "b": 0.0,
                },
                "opponent_b": {
                    "f": 1.0,
                    "c": 0.0,
                    "b": 0.0,
                }
            },
            "three": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                },
                "opponent_b": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                }
            }
        }
    }

    def __init__(self, path="simple_ai_data.txt"):
        super().__init__(path)


class BluffingAIData(DataHolder):
    """Bluffing AI data structure holder"""
    default_data = {
        "opener_first_move": {
            "one": {
                "f": 0.0,
                "c": 1.0,
                "b": 0.0,
            },
            "two": {
                "f": 0.0,
                "c": 1.0,
                "b": 0.0,
            },
            "three": {
                "f": 0.0,
                "c": 0.0,
                "b": 1.0,
            }
        },
        "dealer_first_move": {
            "one": {
                "opponent_c": {
                    "f": 2,
                    "c": 0.0,
                    "b": 1,
                },
                "opponent_b": {
                    "f": 1.0,
                    "c": 0.0,
                    "b": 0.0,
                }
            },
            "two": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 1.0,
                    "b": 0.0,
                },
                "opponent_b": {
                    "f": 2,
                    "c": 0.0,
                    "b": 1,
                }
            },
            "three": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                },
                "opponent_b": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                }
            }
        },
        "opener_second_move": {
            "one": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 1.0,
                    "b": 0.0,
                },
                "opponent_b": {
                    "f": 1.0,
                    "c": 0.0,
                    "b": 0.0,
                }
            },
            "two": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 1.0,
                    "b": 0.0,
                },
                "opponent_b": {
                    "f": 1.0,
                    "c": 0.0,
                    "b": 0.0,
                }
            },
            "three": {
                "opponent_c": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                },
                "opponent_b": {
                    "f": 0.0,
                    "c": 0.0,
                    "b": 1.0,
                }
            }
        }
    }

    def __init__(self, path="bluffing_ai_data.txt"):
        super().__init__(path)
