class Card:
    def __init__(self, averse, reverse, stage, nxt_rep):
        self.averse = averse
        self.reverse = reverse
        self.stage = stage
        self.nxt_rep = nxt_rep
    def update_nxt_rep(self):
        pass
    def update_stage(self, progr):
        if progr and self.stage < 5:
            self.stage += 1
        elif not progr and self.stage > 1:
            self.stage -= 1    
    def edit_averse(self, new_averse):
        self.averse = new_awerse
    def edit_reverse(self, new_reverse):
        self.reverse = new_reverse
class Deck:
    def __init__(self, name, card_list):
        self.name = name
        self.card_set = card_set
    def add_card(self, new_card):
        self.card_set.add(new_card)
    def remove_card(self, target_card):
        self.card_set.remove(target_card)
    #реализовать создание и удаление вспомогательных списков для проведения игры
