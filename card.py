"""Card class module"""
from dataclasses import dataclass


@dataclass
class Card:
    """Card class, inspired by black jack done a while ago"""
    value: int
    face_up: bool = True

    def __str__(self):
        return f"[{self.value:}]" if self.face_up else "[■]"

    def flip_face(self):
        """Flips to opposite face, mainly unused now"""
        self.face_up = not self.face_up