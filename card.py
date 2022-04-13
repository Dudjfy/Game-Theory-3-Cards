class Card:
    def __init__(self, value: int):
        self.value = value
        self.face_up = True

    def __str__(self):
        return f"[{self.value:}]" if self.face_up else "[■]"

    def flip_face(self):
        self.face_up = not self.face_up
