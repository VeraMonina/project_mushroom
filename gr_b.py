class Card:
    def __init__(self, averse, reverse, stage, nxt_rep):
        self.averse = averse
        self.reverse = reverse
        self.stage = stage
        self.nxt_rep = nxt_rep
    def update_nxt_rep(self):
        pass
    def update_stage(self):
        self.stage += 1
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
'''    
c1, c2, c3 = Card(12, 24, 1, 0), Card(12, 24, 1, 1), Card(12, 24, 1, 2)
d1 = Deck([c1, c2, c3])
for c in d1.card_list:
    print(c.nxt_rep)
d1.delete_card(c2)
for c in d1.card_list:
    print(c.nxt_rep)
'''