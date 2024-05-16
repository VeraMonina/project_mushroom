from datetime import *
from queue import *

class My_Queue(Queue):
    def size(self):
        return len(self.queue)

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
    def __init__(self, name, card_set):
        self.name = name
        self.card_set = card_set
    def add_card(self, new_card):
        self.card_set.add(new_card)
    def remove_card(self, target_card):
        self.card_set.remove(target_card)
    def play(self):
        game_deck = My_Queue() #узнать про prioritized queue и возможно её и сделать
        for card in self.card_set:
            if True: #заменить на условие необходимости повторить карточку
                game_deck.put(card)
        while game_deck.size() > 0:
            curr_card = game_deck.get()
            print(curr_card.averse)
            if input().lower() == curr_card.reverse:
                print('correct')
            else:
                print('incorrect, ' + curr_card.reverse)
                game_deck.put(curr_card)
        print('done')

c1 = Card('дом', 'maison', 1, 1)
c2 = Card('вокзал', 'gare', 1, 1)
d = Deck('french words', (c1, c2))
d.play()
