class OpenerBetting:
    def __init__(self, bluff_on_1=0, bluff_on_2=0, bluff_on_3=0):
        self.bluff_on_1 = bluff_on_1
        self.bluff_on_2 = bluff_on_2
        self.bluff_on_3 = bluff_on_3


class DealerBetting:
    def __init__(self, bluff_on_1=1/3, bluff_on_2=1/3, bluff_on_3=0):
        self.bluff_on_1 = bluff_on_1
        self.bluff_on_2 = bluff_on_2
        self.bluff_on_3 = bluff_on_3