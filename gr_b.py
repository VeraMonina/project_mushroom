from datetime import *
from queue import *
import pygame
import csv

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
        if progr and self.stage == 7:
            self.stage += 1
            learned_cards += 1
        elif progr and self.stage < 7:
            self.stage += 1
        elif not progr and self.stage == 8:
            self.stage -= 1
            learned_cards -= 1
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
    def __init__(self, name, card_list):
        self.name = name
        self.card_list = card_list
    def add_card(self, new_card):
        self.card_list.append(new_card)
    def remove_card(self, target_card):
        self.card_list.remove(target_card)
    def extra_rep(self):
        for curr_card in self.card_list:
            while True: #может это тоже неоч?
                print(curr_card.averse) #ЗАМЕНА: ФРОНТ ВЫВОД АВЕРСА КАРТОЧКИ
                if input().lower() == curr_card.reverse.lower(): #возможно инпут поменять на тамошнее что-то
                    print('correct') #ЗАМЕНА: ФРОНТ ВЫВОД СООБЩЕНИЯ 'Правильно'
                    break
                else:
                    print('incorrect, ' + curr_card.reverse) #ЗАМЕНА: ФРОНТ ВЫВОД 'Неправильно, ' + РЕВЕРС КАРТОЧКИ  
    def play(self):
        game_deck = My_Queue() #узнать про prioritized queue и возможно её и сделать
        played = {} #проверить нельзя ли вообще убрать этот play
        for card in self.card_list:
            if card.nxt_rep <= datetime.now():
                game_deck.put(card)
        while game_deck.size() > 0:
            curr_card = game_deck.get()
            if curr_card.nxt_rep > datetime.now():
                played[(averse, reverse)] = (curr_card.stage, curr_card.nxt_rep) #это вообще нормально?
                
            elif curr_card.stage == 1:
                print(curr_card.averse, curr_card.reverse, sep=' - ') #ЗАМЕНА: ВЫВОД В ФОРМАТЕ АВЕРС - РЕВЕРС
                curr_card.update_stage(True)
                curr_card.update_nxt_rep()
                game_deck.put(curr_card)
                if input():
                    continue
            else:
                print(curr_card.averse) #ЗАМЕНА: ВЫВОД АВЕРСА
                if input().lower() == curr_card.reverse.lower():
                    print('correct') #ЗАМЕНА: ВЫВОД 'Правильно'
                    curr_card.update_stage(True)
                    curr_card.update_nxt_rep() 
                    if curr_card.stage <= 3:
                        game_deck.put(curr_card)
                    else:
                        played[(curr_card.averse, curr_card.reverse)] = (curr_card.stage, curr_card.nxt_rep)
                else:
                    print('incorrect, ' + curr_card.reverse) #ЗАМЕНА: ВЫВОД 'Неправильно, ' + РЕВЕРС КАРТОЧКИ
                    curr_card.update_stage(False)
                    curr_card.nxt_rep = datetime.now()
                    game_deck.put(curr_card)
        if len(played) != 0:
            for card in self.card_list:
                card_data = (card.averse, card.reverse)
                new_stage, new_nxt_rep = played[card_data]
                card.edit_state(new_stage, new_nxt_rep)
        print('no more cards, wanna study some more?') #ЗАМЕНА: ВЫВОД 'Нет карточек для повторения. Хотите позаниматься дополнительно?'
        answer = input() #ЗАМЕНА: кнопки 'Да' и 'Нет'. Если нажал да, то self.extra_rep(), если нет, то на главный экран.
        if answer == 'yes': #тут тоже, соответственно
            self.extra_rep()

#буду делать файлик
#надо ли запретить его редактирование???
            
def count_achievements():
    return learned_cards - (learned_cards % 50)

def upload_information():
    with open('all_data.tsv', 'r') as f: #получаем информацию о колодах и карточках, чтобы их проинтициализировать и вывести на экран
        reader = csv.DictReader(f, delimiter='\t')
        for dictionary in reader:
            deck_name, averse, reverse, stage, nxt_rep = reader['Deck name'], reader['Averse'], reader['Reverse'], reader['Stage'], reader['Next repeat']
            new_card = Card(averse, reverse, stage, nxt_rep)
            for deck in super_deck:
                if deck.name == deck_name:
                    deck.card_list.add(new_card)
                    break
            else:
                super_deck.append(Deck(deck_name, [new_card]))
    
    with open('achievements.txt', 'r') as f: #получаем информацию о достижениях
        learned_cards = int(f.readline())    

def download_information():
    with open('all_data.tsv', 'w') as f: #сохраняем всю информацию о колодах и карточках
        f.write('Deck name' + '\t' + 'Averse' + '\t' + 'Reverse' + '\t' + 'Stage' + '\t' + 'Next repeat')
        for deck in super_deck:
            for card in deck:
                f.write(deck.name + '\t' + card.averse + '\t' + card.reverse + '\t' + card.stage + '\t' + card.nxt_rep + '\n')
    
    with open('achievements.txt', 'w') as f: #сохраняем информацию о достижениях
        f.write(learned_cards)

class Drawer():
    def __init__(self, window):
        self.window = window
        self.isdestroyed = False

    def _check_quit(self, event):
        if event.type == pygame.QUIT:
            download_information()
            pygame.quit()
            exit()

    def _render_font(self, text, sz):
        return pygame.font.SysFont('Verdana', sz).render(text, True, Clrs.black)

    def _draw_rect(self, text, scale, pos, sz, color):
        button_rect = pygame.Rect(pos, scale)
        pygame.draw.rect(self.window, color, button_rect)
        button_text = self._render_font(text, sz)
        text_pos = button_text.get_rect(center=pygame.Rect(pos, scale).center)
        self.window.blit(button_text, text_pos)

    def _draw_text(self, text, pos, sz):
        item_text = self._render_font(text, sz)
        self.window.blit(item_text, pos)

    def _draw_image(self, asset, scale, pos):
        myimage = pygame.image.load(f'assets/{asset}')
        myimage = pygame.transform.scale(myimage, scale)
        self.window.blit(myimage, pos)

    def _draw_input(self, scale, pos, text, isclicked):
        col = Clrs.black if isclicked else Clrs.white
        self._draw_rect('', (scale[0] + 4, scale[1] + 4), (pos[0] - 2, pos[1] - 2), 0, col)
        self._draw_rect(text, scale, pos, 20, Clrs.lgray)

    # override
    def _set_menu(self):
        return

    # override
    def start(self):
        return
                            

class Clrs:
    white = (255, 255, 255)
    black = (0, 0, 0)
    lgray = (200, 200, 200)
    gray = (100, 100, 100)
    pink = (255, 150, 150)
    red = (255, 0, 0)
    green = (0, 255, 0)
    brown = (210, 180, 140)
    blue = (40, 40, 220)

class Square:
    def __init__(self, scale, pos):
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = pos[0] + scale[0]
        self.y2 = pos[1] + scale[1]

    def contains(self, pos):
        return self.x1 <= pos[0] <= self.x2 and \
               self.y1 <= pos[1] <= self.y2

class MainMenu(Drawer):
    
    ''' #этого по идее не должно существовать
        def __add_reverse_catalog(self, i):
            obj = {}
            for j in lst[i].lang:
                obj[lst[i].lang[j]] = j
            lst.append(Catalog(f'{lst[i].name} reversed', obj))
    '''    
    
    def __draw_catalog_item(self, catalog, pos):
        self._draw_rect('Учить', (50, 25), pos, 14, Clrs.blue)
        self._draw_rect(catalog.name, (700, 25), (pos[0]+52, pos[1]), 16, Clrs.lgray)
        self._draw_image('trashcan.jpg', (25, 25), (pos[0]+754, pos[1]))
        self._draw_image('refresh.png', (25, 25), (pos[0]+781, pos[1]))

    def _set_menu(self):
        self.window.fill(Clrs.white)
        actions = []
        cnt = 1
        for i in super_deck:
            self.__draw_catalog_item(i, (100, (cnt) * 30))
            actions.append(Square((50, 25), (100, (cnt) * 30)))
            actions.append(Square((700, 25), (152, (cnt) * 30)))
            actions.append(Square((25, 25), (854, (cnt) * 30)))
            actions.append(Square((25, 25), (881, (cnt) * 30)))
            cnt += 1
        self._draw_rect('Добавить', (1000, 50), (0, 550), 18, Clrs.white)
        actions.append(Square((1000, 50), (0, 550)))
        self._draw_image('cup.png', (30, 30), (10, 10))
        actions.append(Square((30, 30), (10, 10)))
        pygame.display.update()
        return actions
    
    def start(self):
        actions = self._set_menu()
        #pygame.display.flip()
        while not self.isdestroyed:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.contains(event.pos):
                            if act == len(actions) - 2:
                                self.isdestroyed = True
                                AddDeck(self.window).start()
                                break
                            if act == len(actions) - 1:
                                self.isdestroyed = True
                                Achievements(self.window).start()
                                break
                            if act % 4 == 0:
                                #Кнопка учить, нажатие на которую вызывает d.play(), где d - колода, которую человек хочет учить
                                pass # TODO #ЧТО ТУДУ?...
                            if act % 4 == 1:
                                self.isdestroyed = True
                                EditDeck(self.window).start(act // 4)
                                break
                            if act % 4 == 2:
                                super_deck.pop(act // 4)
                                self._set_menu()
                            if act % 4 == 3:
                                self.__add_reverse_catalog(act // 4)
                                actions = self._set_menu()
                            

class AddDeck(Drawer):
    def _set_menu(self):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect('Создание колоды', (200, 20), (400, 20), 24, Clrs.white)
        isclicked = False
        text = ''
        self._draw_input((400, 50), (300, 200), text, isclicked)
        actions.append(Square((400, 50), (300, 200)))
        self._draw_rect('Сохранить', (300, 50), (350, 500), 18, Clrs.white)
        actions.append(Square((300, 50), (350, 500)))
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        pygame.display.update()
        return actions
    
    def start(self):
        actions, text, isclicked = self._set_menu(), '', False
        #pygame.display.flip()
        while not self.isdestroyed:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isclicked = False
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.contains(event.pos):
                            if act == 0:
                                isclicked = True
                            if act == 1:
                                if len(text) == 0:
                                    self._draw_rect('Поле не должно быть пустым',
                                        (250, 40), (375, 400), 14, Clrs.gray)
                                else:
                                    super_deck.append(Deck(text, []))
                                    MainMenu(self.window).start()
                                    break
                            if act == 2:
                                MainMenu(self.window).start()
                                break
                if event.type == pygame.KEYDOWN and isclicked:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                self._draw_input((400, 50), (300, 200), text, isclicked)
                pygame.display.update()

#ГДЕ УДАДЕНИЕ КОЛОДЫ

class EditDeck(Drawer):
    def __draw_card(self, i, j, y):
        for card in super_deck[i].card_list:
            if card.reverse == j:
                reverse = card.reverse
                break
        self._draw_rect(f'{j} - {reverse}', (500, 50), (235, y), 18, Clrs.lgray)
        self._draw_image('edit.png', (30, 30), (740, y+10))

    def __set_menu(self, ind):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect(f'Редактирование колоды "{super_deck[ind].name}"', (1000, 20), (0, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        self._draw_image('back.png', (25, 25), (900, 550))
        actions.append(Square((25, 25), (900, 550)))
        self._draw_image('forw.png', (25, 25), (930, 550))
        actions.append(Square((25, 25), (930, 550)))
        self._draw_image('plus.png', (50, 50), (475, 540))
        actions.append(Square((50, 50), (475, 540)))
        cnt = 1
        averse_list = []
        for card in super_deck[ind].card_list:
            averse_list.append(card.averse)
        for j in averse_list[self.offset : self.offset + 8]:
            y = 60 * cnt
            self.__draw_card(ind, j, y)
            actions.append(Square((40, 40), (740, y + 5)))
            cnt += 1
        pygame.display.update()
        return actions
    
    def start(self, ind):
        self.offset = 0
        page = 0
        actions = self.__set_menu(ind)
        #pygame.display.flip()
        while not self.isdestroyed:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.contains(event.pos):
                            if act > 3:
                                self.isdestroyed = True
                                averse_list = []
                                for card in super_deck[ind].card_list:
                                    averse_list.append(card.averse)
                                k = averse_list[act - 4]
                                EditCard(self.window).start(ind, k)
                                break
                            if act == 0:
                                self.isdestroyed = True
                                MainMenu(self.window).start()
                                break
                            if act == 1:
                                self.offset = max(0, self.offset - 8)
                                page = max(0, page - 1)
                                self.__set_menu(ind)
                            if act == 2:
                                if self.offset + 8 < len(super_deck[ind].card_list):
                                    self.offset = min(len(super_deck[ind].card_list), self.offset + 8)
                                    page += 1
                                    self.__set_menu(ind)
                            if act == 3:
                                self.isdestroyed = True
                                AddCard(self.window).start(ind)
                                break


class EditCard(Drawer):
    def _set_menu(self, ind, word):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect('Редактирование карточки', (200, 20), (400, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        isclicked = [False, False]
        text = [word, super_deck[ind].card_list[word]]
        self._draw_input((400, 50), (300, 200), text[0], isclicked[0])
        actions.append(Square((400, 50), (300, 200)))
        self._draw_input((400, 50), (300, 300), text[1], isclicked[1])
        actions.append(Square((400, 50), (300, 300)))
        pygame.display.update()
        return actions

    def start(self, ind, word):
        actions = self._set_menu(ind, word)
        for card in super_deck[ind].card_list:
            if card.averse == word:
                word_reverse = card.reverse
                break
        text = [word, word_reverse]
        isclicked = [False, False]
        #pygame.display.flip()
        while not self.isdestroyed:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isclicked = [False, False]
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.contains(event.pos):
                            if act == 0:
                                self.isdestroyed = True
                                EditDeck(self.window).start(ind)
                                break
                            if act == 1:
                                isclicked = [True, False]
                            if act == 2:
                                isclicked = [False, True]
                if event.type == pygame.KEYDOWN:
                    for i in range(2):
                        if isclicked[i]:
                            if event.key == pygame.K_BACKSPACE:
                                text[i] = text[i][:-1]
                            else:
                                text[i] += event.unicode
                self._draw_input((400, 50), (300, 200), text[0], isclicked[0])
                self._draw_input((400, 50), (300, 300), text[1], isclicked[1])
                pygame.display.update()
                            
class AddCard(Drawer):
    def _set_menu(self, ind):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect('Добавление карточки', (200, 20), (400, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        isclicked = [False, False]
        text = ['', '']
        self._draw_input((400, 50), (300, 200), text[0], isclicked[0])
        actions.append(Square((400, 50), (300, 200)))
        self._draw_input((400, 50), (300, 300), text[1], isclicked[1])
        actions.append(Square((400, 50), (300, 300)))
        pygame.display.update()
        return actions

    def start(self, ind):
        actions = self._set_menu(ind)
        text = ['', '']
        isclicked = [False, False]
        #pygame.display.flip()
        while not self.isdestroyed:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isclicked = [False, False]
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.contains(event.pos):
                            if act == 0:
                                self.isdestroyed = True
                                EditDeck(self.window).start(ind)
                                break
                            if act == 1:
                                isclicked = [True, False]
                            if act == 2:
                                isclicked = [False, True]
                if event.type == pygame.KEYDOWN:
                    for i in range(2):
                        if isclicked[i]:
                            if event.key == pygame.K_BACKSPACE:
                                text[i] = text[i][:-1]
                            else:
                                text[i] += event.unicode
                self._draw_input((400, 50), (300, 200), text[0], isclicked[0])
                self._draw_input((400, 50), (300, 300), text[1], isclicked[1])
                pygame.display.update()                            

#УДАЛЕНИЕ КАРТОЧКИ ГДЕ

class Achievements(Drawer):
    def _set_menu(self):
        self.window.fill(Clrs.white)
        # TODO
        if count_achievements() == 50:
            pass
        elif count_achievements() == 100:
            pass
        #и так доделать для остальных, последний случай - >= сколько-то, а не только само это число
        pygame.display.flip()

    def start(self):
        self._set_menu()
        #pygame.display.flip()
        

class MyGame:
    SIZE = (1000, 600)

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(MyGame.SIZE)
        self.main = MainMenu(self.window)

    def start(self):
        self.main.start()
        upload_information()

super_deck = []
learned_cards = 0
game = MyGame()
game.start()
