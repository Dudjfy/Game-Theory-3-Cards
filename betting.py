"""Old system betting and bluffing chances data classes reworked, might be unused now"""

from dataclasses import dataclass


@dataclass
class OpenerBetting:
    """Opener betting, old system"""
    bluff_on_1: float = 0
    bluff_on_2: float = 0
    bluff_on_3: float = 0


@dataclass
class DealerBetting:
    """Dealer betting, old system"""
    bluff_on_1: float = 1 / 3
    bluff_on_2: float = 1 / 3
    bluff_on_3: float = 0
