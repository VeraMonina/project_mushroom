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
        if self.stage <= 3:
            self.nxt_rep = datetime.now()
        elif self.stage == 4:
            self.nxt_rep = datetime.now() + timedelta(hours=1)
        elif self.stage == 5:
            self.nxt_rep = datetime.now() + timedelta(hours=8)
        elif self.stage == 6:
            self.nxt_rep = datetime.now() + timedelta(days=1)
        elif self.stage == 7:
            self.nxt_rep = datetime.now() + timedelta(days=3)
        else:
            self.nxt_rep == datetime.now() + timedelta(weeks=1)
    def update_stage(self, progr):
        if progr and self.stage < 8:
            self.stage += 1
        elif not progr and self.stage > 3:
            self.stage -= 1
    def edit_averse(self, new_averse):
        self.averse = new_awerse
    def edit_reverse(self, new_reverse):
        self.reverse = new_reverse
    def edit_state(self, new_stage, new_nxt_rep): #это запрещённая техника, нужно ли прятать? или нужно или сливать с update-ами?
        self.stage = new_stage
        self.nxt_rep = new_nxt_rep

class Deck:
    def __init__(self, name, card_set):
        self.name = name
        self.card_set = card_set
    def add_card(self, new_card):
        self.card_set.add(new_card)
    def remove_card(self, target_card):
        self.card_set.remove(target_card)
    def extra_rep(self):
        for curr_card in self.card_set:
            while True: #может это тоже неоч?
                print(curr_card.averse)
                if input().lower() == curr_card.reverse.lower():
                    print('correct')
                    break
                else:
                    print('incorrect, ' + curr_card.reverse)          
    def play(self):
        game_deck = My_Queue() #узнать про prioritized queue и возможно её и сделать
        played = {}
        for card in self.card_set:
            if card.nxt_rep <= datetime.now():
                game_deck.put(card)
        while game_deck.size() > 0:
            curr_card = game_deck.get()
            if curr_card.nxt_rep > datetime.now():
                played[(averse, reverse)] = (curr_card.stage, curr_card.nxt_rep) #это вообще нормально?
            elif curr_card.stage == 1:
                print(curr_card.averse, curr_card.reverse, sep=' - ')
                curr_card.update_stage(True)
                curr_card.update_nxt_rep()
                game_deck.put(curr_card)
                if input():
                    continue
            else:
                print(curr_card.averse)
                if input().lower() == curr_card.reverse.lower():
                    print('correct')
                    curr_card.update_stage(True)
                    curr_card.update_nxt_rep() 
                    if curr_card.stage <= 3:
                        game_deck.put(curr_card)
                    else:
                        played[(curr_card.averse, curr_card.reverse)] = (curr_card.stage, curr_card.nxt_rep)
                else:
                    print('incorrect, ' + curr_card.reverse)
                    curr_card.update_stage(False)
                    curr_card.nxt_rep = datetime.now()
                    game_deck.put(curr_card)
        if len(played) != 0:
            for card in self.card_set:
                card_data = (card.averse, card.reverse)
                print(self.card_set)
                new_stage, new_nxt_rep = played[card_data]
                card.edit_state(new_stage, new_nxt_rep)
        print('no more cards, wanna study some more?')
        answer = input()
        if answer == 'yes':
            self.extra_rep()
'''
c1 = Card('спасибо', 'merci', 1, datetime.now())
c2 = Card('кошмар', 'cauchemard', 1, datetime.now())
d = Deck('french words', (c1, c2))
while True:
    d.play()
    for card in d.card_set:
        print(card.averse, card.reverse, card.stage, card.nxt_rep)
'''
