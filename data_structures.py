import json


class SimpleAiData:
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
        self.data = None
        self.path = path
        self.load()

    def reset_to_default_data(self):
        self.data = self.default_data

    def load(self):
        with open(self.path, "r") as json_file:
            self.data = json.load(json_file)

    def save(self):
        with open(self.path, "w") as json_file:
            json.dump(self.data, json_file)

    def print_whole_with_indents(self, indent=4):
        print(json.dumps(self.data, indent=indent))

    def get_dict_element_by_keys_recursively(self, args, msg=None):
        if len(args) <= 0:
            return msg

        if msg is None:
            return self.get_dict_element_by_keys_recursively(args[1:], msg=self.data[args[0]])
        return self.get_dict_element_by_keys_recursively(args[1:], msg=msg[args[0]])

    def get_dict_element_by_keys_looping(self, args):
        msg = self.data
        for arg in args:
            msg = msg[arg]
        return msg

    def print_element_by_keys(self, args):
        # print(self.get_dict_element_by_keys_recursively(args))
        print(self.get_dict_element_by_keys_looping(args))

    def set_element_by_keys(self, args, new_value=None):
        data = self.data
        last_key = args[-1]
        for k in args[:-1]:  # when assigning drill down to *second* last key
            data = data[k]
        data[last_key] = new_value

