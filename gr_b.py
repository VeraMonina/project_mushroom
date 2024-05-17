from datetime import *
from queue import *

class My_Queue(Queue):
    def size(self):
        return len(self.queue)

class Card:
    def __init__(self, averse, reverse, stage, substage, nxt_rep):
        self.averse = averse
        self.reverse = reverse
        self.stage = stage
        self.substage = substage
        self.nxt_rep = nxt_rep
    def update_nxt_rep(self):
        if self.stage == 1 and self.substage == 1:
            self.nxt_rep = datetime.now()
        elif self.stage == 1:
            print(self.nxt_rep, 'OLD, IN METHOD')
            self.nxt_rep = datetime.now() + timedelta(hours=1)
            print(self.nxt_rep, 'NEW, IN METHOD')
        elif self.stage == 2:
            self.nxt_rep = datetime.now() + timedelta(hours=8)
        elif self.stage == 3:
            self.nxt_rep = datetime.now() + timedelta(days=1)
        elif self.stage == 4:
            self.nxt_rep = datetime.now() + timedelta(days=3)
        else:
            self.nxt_rep == datetime.now() + timedelta(weeks=1)
    def update_stage(self, progr):
        if progr and self.stage < 5:
            self.stage += 1
            self.substage = 1
        elif not progr and self.stage > 1:
            self.stage -= 1
            self.substage = 3
    def update_substage(self, progr):
        if progr and self.substage < 3:
            self.substage += 1
        elif not progr and self.substage > 1:
            self.substage -= 1
        else:
            self.update_stage(progr)
    def edit_averse(self, new_averse):
        self.averse = new_awerse
    def edit_reverse(self, new_reverse):
        self.reverse = new_reverse
    def edit_state(self, new_stage, new_substage, new_nxt_rep): #это запрещённая техника, нужно ли прятать? или нужно или сливать с update-ами?
        self.stage = new_stage
        self.substage = new_substage
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
                played[(averse, reverse)] = (curr_card.stage, curr_card.substage, curr_card.nxt_rep) #это вообще нормально?
            else:
                print(curr_card.averse)
                if input().lower() == curr_card.reverse.lower():
                    print('correct')
                    curr_card.update_nxt_rep() #так как я меняю местами обновления, количество подстадий должно быть меньше на 1 !!!
                    curr_card.update_substage(True)
                    if curr_card.stage == 1 and curr_card.substage == 1:
                        game_deck.put(curr_card)
                    else:
                        played[(curr_card.averse, curr_card.reverse)] = (curr_card.stage, curr_card.substage, curr_card.nxt_rep) #видимо тут проблема с nxt_rep, когда карточка свежая
                else:
                    print('incorrect, ' + curr_card.reverse)
                    curr_card.update_substage(False)
                    curr_card.nxt_rep = datetime.now()
                    game_deck.put(curr_card)
        if len(self.card_set) != 0:
            for card in self.card_set:
                card_data = (card.averse, card.reverse)
                print(self.card_set)
                new_stage, new_substage, new_nxt_rep = played[card_data] #не понимаю в чём проблема
                card.edit_state(new_stage, new_substage, new_nxt_rep)
        print('no more cards, wanna study some more?')
        answer = input()
        if answer == 'yes':
            self.extra_rep()

c1 = Card('дом', 'maison', 1, 1, datetime.now())
c2 = Card('вокзал', 'gare', 1, 1, datetime.now())
d = Deck('french words', (c1, c2))
while True:
    d.play()
    for card in d.card_set:
        print(card.averse, card.reverse, card.stage, card.substage, card.nxt_rep)
