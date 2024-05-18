from datetime import *
from queue import *
import pygame as pg
import pygame
import csv
import random


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

    def edit_state(self, new_stage, new_nxt_rep):
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
            while True:  # может это тоже неоч?
                print(curr_card.averse)  # ЗАМЕНА: ФРОНТ ВЫВОД АВЕРСА КАРТОЧКИ
                if input().lower() == curr_card.reverse.lower():
                    # возможно инпут поменять на тамошнее что-то
                    print('correct')
                    # ЗАМЕНА: ФРОНТ ВЫВОД СООБЩЕНИЯ 'Правильно'
                    break
                else:
                    print('incorrect, ' + curr_card.reverse)
                    # ЗАМЕНА: ФРОНТ ВЫВОД 'Неправильно, ' + РЕВЕРС КАРТОЧКИ

    def play(self):
        game_deck = My_Queue()
        played = {}
        for card in self.card_list:
            if card.nxt_rep <= datetime.now():
                game_deck.put(card)
        while game_deck.size() > 0:
            curr_card = game_deck.get()
            if curr_card.nxt_rep > datetime.now():
                played[(averse, reverse)] = (curr_card.stage,
                                             curr_card.nxt_rep)
                # это вообще нормально?

            elif curr_card.stage == 1:
                print(curr_card.averse, curr_card.reverse, sep=' - ')
                # ЗАМЕНА: ВЫВОД В ФОРМАТЕ АВЕРС - РЕВЕРС
                curr_card.update_stage(True)
                curr_card.update_nxt_rep()
                game_deck.put(curr_card)
                if input():
                    continue
            else:
                print(curr_card.averse)  # ЗАМЕНА: ВЫВОД АВЕРСА
                if input().lower() == curr_card.reverse.lower():
                    print('correct')  # ЗАМЕНА: ВЫВОД 'Правильно'
                    curr_card.update_stage(True)
                    curr_card.update_nxt_rep()
                    if curr_card.stage <= 3:
                        game_deck.put(curr_card)
                    else:
                        played[(curr_card.averse, curr_card.reverse)] \
                            = (curr_card.stage, curr_card.nxt_rep)
                else:
                    print('incorrect, ' + curr_card.reverse)
                    # ЗАМЕНА: ВЫВОД 'Неправильно, ' + РЕВЕРС КАРТОЧКИ
                    curr_card.update_stage(False)
                    curr_card.nxt_rep = datetime.now()
                    game_deck.put(curr_card)
        if len(played) != 0:
            for card in self.card_list:
                card_data = (card.averse, card.reverse)
                new_stage, new_nxt_rep = played[card_data]
                card.edit_state(new_stage, new_nxt_rep)
        print(
            'no more cards, wanna study some more?')  # ЗАМЕНА:
        # ВЫВОД 'Нет карточек для повторения.
        # Хотите позаниматься дополнительно?'
        answer = input()  # ЗАМЕНА: кнопки 'Да' и 'Нет'.
        # Если нажал да, то self.extra_rep(), если нет, то на главный экран.
        if answer == 'yes':  # тут тоже, соответственно
            self.extra_rep()


# буду делать файлик
# надо ли запретить его редактирование???

def count_achievements():
    return learned_cards - (learned_cards % 50)


def upload_information():
    with open('all_data.tsv',
              'r') as f:
        # получаем информацию о колодах и карточках,
        # чтобы их проинтициализировать и вывести на экран
        reader = csv.DictReader(f, delimiter='\t')
        for dictionary in reader:
            deck_name, averse, reverse, stage, nxt_rep = \
              dictionary['Deck name'], dictionary['Averse'],
            dictionary['Reverse'], dictionary['Stage'],
            dictionary['Next repeat']
            print(deck_name, averse, reverse, stage, nxt_rep)
            new_card = Card(averse, reverse, stage, nxt_rep)
            finded = False
            for i in range(len(super_deck)):
                if super_deck[i].name == deck_name:
                    finded = True
                    deck.card_list.add(new_card)
                    break
            if not finded:
                super_deck.append(Deck(deck_name, [new_card]))

    with open('achievements.txt', 'r') as f:
        # получаем информацию о достижениях
        learned_cards = int(f.readline())


def download_information():
    with open('all_data.tsv', 'w') as f:
        # сохраняем всю информацию о колодах и карточках
        f.write(
            'Deck name' + '\t' + 'Averse' + '\t' +
            'Reverse' + '\t' + 'Stage' + '\t' + 'Next repeat' + '\n')
        for deck in super_deck:
            for card in deck.card_list:
                f.write(deck.name + '\t' +
                        card.averse + '\t' + card.reverse + '\t' +
                        str(card.stage) + '\t' + str(card.nxt_rep) + '\n')
                print(deck.name + '\t' + card.averse + '\t' +
                      card.reverse + '\t' + str(card.stage) + '\t' +
                      str(card.nxt_rep) + '\n')

    with open('achievements.txt', 'w') as f:
        # сохраняем информацию о достижениях
        f.write(str(learned_cards))


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
        return pygame.font.SysFont('Verdana', sz).\
            render(text, True, Clrs.black)

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
        self._draw_rect('', (scale[0] + 4, scale[1] + 4),
                        (pos[0] - 2, pos[1] - 2), 0, col)
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
        self._draw_rect(catalog.name, (700, 25),
                        (pos[0] + 52, pos[1]), 16, Clrs.lgray)
        self._draw_image('trashcan.jpg', (25, 25),
                         (pos[0] + 754, pos[1]))  # ИКОНКА УДАЛЕНИЯ
        # self._draw_image('refresh.png', (25, 25), (pos[0]+781, pos[1]))

    def _set_menu(self):
        self.window.fill(Clrs.white)
        actions = []
        cnt = 1
        for i in super_deck:
            self.__draw_catalog_item(i, (100, (cnt) * 30))
            actions.append(Square((50, 25), (100, (cnt) * 30)))
            actions.append(Square((700, 25), (152, (cnt) * 30)))
            actions.append(Square((25, 25), (854, (cnt) * 30)))
            # actions.append(Square((25, 25), (881, (cnt) * 30)))
            cnt += 1
        self._draw_rect('Добавить', (1000, 50), (0, 550), 18, Clrs.white)
        actions.append(Square((1000, 50), (0, 550)))
        self._draw_image('cup.png', (30, 30), (10, 10))
        actions.append(Square((30, 30), (10, 10)))
        pygame.display.update()
        return actions

    def start(self):
        actions = self._set_menu()
        # pygame.display.flip()
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
                                super_deck[act // 4].play()
                            if act % 4 == 1:
                                self.isdestroyed = True
                                EditDeck(self.window).start(act // 4)
                                break
                            if act % 4 == 2:
                                super_deck.pop(act // 4)  # УДАЛЕНИЕ
                                self._set_menu()
                            if act % 4 == 3:
                                self.__add_reverse_catalog(act // 4)
                                actions = self._set_menu()


class AddDeck(Drawer):
    def _set_menu(self):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect('Создание колоды',
                        (200, 20), (400, 20), 24, Clrs.white)
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
        # pygame.display.flip()
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
                                    self._draw_rect('Пустое поле',
                                                    (250, 40), (375, 400),
                                                    14, Clrs.gray)
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


# ГДЕ УДАДЕНИЕ КОЛОДЫ (см выше)

class EditDeck(Drawer):
    def __draw_card(self, card, y):
        self._draw_rect(f'{card.averse} - {card.reverse}',
                        (500, 50), (235, y), 18, Clrs.lgray)
        self._draw_image('edit.png', (30, 30), (740, y + 10))
        self._draw_image('trashcan.jpg', (30, 30), (780, y + 10))

    def __set_menu(self, ind):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect(f'Редактирование колоды "{super_deck[ind].name}"',
                        (1000, 20), (0, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        self._draw_image('back.png', (25, 25), (900, 550))
        actions.append(Square((25, 25), (900, 550)))
        self._draw_image('forw.png', (25, 25), (930, 550))
        actions.append(Square((25, 25), (930, 550)))
        self._draw_image('plus.png', (50, 50), (475, 540))
        actions.append(Square((50, 50), (475, 540)))
        cnt = 1
        for card in super_deck[ind].card_list[self.offset: self.offset + 8]:
            y = 60 * cnt
            self.__draw_card(card, y)
            actions.append(Square((40, 40), (740, y + 5)))
            actions.append(Square((40, 40), (780, y + 5)))
            cnt += 1
        pygame.display.update()
        return actions

    def start(self, ind):
        self.offset = 0
        page = 0
        actions = self.__set_menu(ind)
        # pygame.display.flip()
        while not self.isdestroyed:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.contains(event.pos):
                            if act > 3:
                                if act % 2 == 0:
                                    self.isdestroyed = True
                                    EditCard(self.window).\
                                        start(ind, page * 8 + (act - 4) // 2)
                                    break
                                else:  # удаление карточки
                                    super_deck[ind].\
                                        card_list.pop((act - 4) // 2)
                                    self.__set_menu(ind)
                            if act == 0:
                                self.isdestroyed = True
                                MainMenu(self.window).start()
                                break
                            if act == 1:
                                self.offset = max(0, self.offset - 8)
                                page = max(0, page - 1)
                                self.__set_menu(ind)
                            if act == 2:
                                if self.offset + 8 < len(super_deck[ind].
                                                         card_list):
                                    self.offset = \
                                        min(len(super_deck[ind].card_list),
                                            self.offset + 8)
                                    page += 1
                                    self.__set_menu(ind)
                            if act == 3:
                                self.isdestroyed = True
                                AddCard(self.window).start(ind)
                                break


class AddCard(Drawer):
    def _set_menu(self, ind):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect('Добавление \
                        карточки', (200, 20), (400, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        isclicked = [False, False]
        text = ['', '']
        self._draw_input((400, 50), (300, 200), text[0], isclicked[0])
        actions.append(Square((400, 50), (300, 200)))
        self._draw_input((400, 50), (300, 300), text[1], isclicked[1])
        actions.append(Square((400, 50), (300, 300)))
        self._draw_rect('Сохранить', (1000, 20), (0, 550), 20, Clrs.white)
        actions.append(Square((1000, 20), (0, 550)))
        pygame.display.update()
        return actions

    def start(self, ind):
        actions = self._set_menu(ind)
        text = ['', '']
        isclicked = [False, False]
        # pygame.display.flip()
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
                            if act == 3:
                                if len(text[0]) == 0 or len(text[1]) == 0:
                                    self._draw_rect('Пустое поле',
                                                    (250, 40), (375, 450),
                                                    14, Clrs.gray)
                                else:
                                    super_deck[ind].\
                                        add_card(Card(text[0], text[1], 1,
                                                      datetime.now()))
                                    self.isdestroyed = True
                                    EditDeck(self.window).start(ind)
                                    break
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


class EditCard(Drawer):
    def _set_menu(self, ind, iword):
        self.window.fill(Clrs.white)
        card = super_deck[ind].card_list[iword]
        actions = []
        self._draw_rect('Редактирование карточки', (200, 20),
                        (400, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        isclicked = [False, False]
        text = [card.averse, card.reverse]
        self._draw_input((400, 50), (300, 200), text[0], isclicked[0])
        actions.append(Square((400, 50), (300, 200)))
        self._draw_input((400, 50), (300, 300), text[1], isclicked[1])
        actions.append(Square((400, 50), (300, 300)))
        self._draw_rect('Сохранить', (1000, 20), (0, 550), 20, Clrs.white)
        actions.append(Square((1000, 20), (0, 550)))
        pygame.display.update()
        return actions

    def start(self, ind, iword):
        actions = self._set_menu(ind, iword)
        card = super_deck[ind].card_list[iword]
        text = [card.averse, card.reverse]
        isclicked = [False, False]
        # pygame.display.flip()
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
                            if act == 3:
                                if len(text[0]) == 0 or len(text[1]) == 0:
                                    self._draw_rect('Пустое поле',
                                                    (250, 40),
                                                    (375, 450), 14, Clrs.gray)
                                else:
                                    super_deck[ind].\
                                        card_list[iword] = Card(text[0],
                                                                text[1], 1,
                                                                datetime.now())
                                    self.isdestroyed = True
                                    EditDeck(self.window).start(ind)
                                    break
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


# УДАЛЕНИЕ КАРТОЧКИ ГДЕ (реализовала на экране редактирования deck-а)

class Achievements(Drawer):
    def _set_menu(self):
        self.window.fill(Clrs.white)
        # TODO
        pygame.init()
        size_w, size_h = 1000, 600
        screen = pygame.display.set_mode((size_w, size_h))

        yellow = (255, 255, 0)
        orange = (255, 165, 0)
        background = (255, 255, 255)

        r = random.randint(400, 400)
        x, x1 = r, r
        y, y1 = r, r
        a = 100
        b = 35
        c = 85
        d = 50
        e = 65

        FPS = 80
        clock = pygame.time.Clock()

        def star(x, x1, y1, a, b, c, d, e):
            pygame.draw.lines(screen, orange, True,
                              ((x1, y1), (x + a, y1),
                               (x - b, y1 - e), (x1 + d, y1)), 7)
            pygame.draw.lines(screen, orange, True,
                              ((x1 + d, y1 + d), (x1 + c, y1 - e),
                               (x1, y1), (x1 + d, y1)), 7)
            pygame.draw.polygon(screen, yellow,
                                ((x1, y1), (x + a, y1),
                                 (x - b, y1 - e), (x1 + d, y1)))
            pygame.draw.polygon(screen, yellow,
                                ((x1 + d, y1 + d), (x1 + c, y1 - e),
                                    (x1, y1), (x1 + d, y1)))

        while True:
            clock.tick(FPS)
            screen.fill(background)  # сначала цвет, потом движение
            if x1 >= 0 and x + a <= 1000:
                star(x, x1, y1, a, b, c, d, e)
                x += 1
                x1 -= 2
                y1 -= 1
                a += 2
                b += 2
                c += 2
                d += 1
                c += 1
            else:
                quit(screen)
            pygame.display.update()
            pygame.display.flip()
        pygame.init()

        # размер окна
        screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('Achievements')
        GREEN = (0, 69, 36)
        BLUE = (0, 191, 255)

        # низ - трава
        pygame.draw.rect(screen, GREEN, (0, 400, 1000, 200))

        # верх - небо
        pygame.draw.rect(screen, BLUE, (0, 0, 1000, 400))

        # солнце
        sun_surf = pg.image.load('ach_pics/sun.bmp').convert()
        scale = pygame.transform.scale(
            sun_surf, (sun_surf.get_width() // 1.5,
                       sun_surf.get_height() // 1.5))
        sun_rect = sun_surf.get_rect(bottomright=(1100, 350))
        scale.set_colorkey((0, 0, 0))
        screen.blit(scale, sun_rect)
        pg.display.update()

        # облако
        obl_surf = pg.image.load('ach_pics/cloud20.bmp').convert()
        scale = pygame.transform.scale(
            obl_surf, (obl_surf.get_width() // 3,
                       obl_surf.get_height() // 3))
        obl_rect = obl_surf.get_rect(bottomright=(1100, 700))
        scale.set_colorkey((0, 0, 0))
        screen.blit(scale, obl_rect)
        pg.display.update()

        # облако2
        obl2_surf = pg.image.load('ach_pics/cloud20.bmp').convert()
        scale = pygame.transform.scale(
            obl2_surf, (obl2_surf.get_width() // 4,
                        obl2_surf.get_height() // 4))
        obl2_rect = obl2_surf.get_rect(bottomright=(1600, 750))
        scale.set_colorkey((0, 0, 0))
        screen.blit(scale, obl2_rect)
        pg.display.update()
        if count_achievements() == 50:
            def reward_fly_agaric_1():
                mush_fly_surf = pg.image.load('ach_pics/mush.bmp').convert()
                mush_fly_rect = mush_fly_surf.get_rect(bottomright=(700, 550))
                mush_fly_surf.set_colorkey((0, 0, 0))
                screen.blit(mush_fly_surf, mush_fly_rect)
                pg.display.update()
                return reward_fly_agaric_1
        elif count_achievements() == 100:
            def reward_fly_agaric_2():
                mush_fly_surf = pg.image.load('ach_pics/mush.bmp').convert()
                mush_fly_rect = mush_fly_surf.get_rect(bottomright=(700, 550))
                mush_fly_surf.set_colorkey((0, 0, 0))
                screen.blit(mush_fly_surf, mush_fly_rect)
                pg.display.update()

                scale = pygame.transform.scale(
                    mush_fly_surf, (mush_fly_surf.get_width() // 2,
                                    mush_fly_surf.get_height() // 2))
                scale_rect = scale.get_rect(center=(350, 450))
                screen.blit(scale, scale_rect)
                pygame.display.update(mush_fly_rect)
                pygame.time.wait(1000)
                return reward_fly_agaric_2
        elif count_achievements() == 150:
            def reward_fly_agaric_3():
                mush_fly_surf = pg.image.load('ach_pics/mush.bmp').convert()
                mush_fly_rect = mush_fly_surf.get_rect(bottomright=(700, 550))
                mush_fly_surf.set_colorkey((0, 0, 0))
                screen.blit(mush_fly_surf, mush_fly_rect)
                pg.display.update()

                scale = pygame.transform.scale(
                    mush_fly_surf, (mush_fly_surf.get_width() // 2,
                                    mush_fly_surf.get_height() // 2))
                scale_rect = scale.get_rect(center=(350, 450))
                screen.blit(scale, scale_rect)
                pygame.display.update(mush_fly_rect)
                pygame.time.wait(1000)

                scale = pygame.transform.scale(
                    mush_fly_surf, (mush_fly_surf.get_width() // 1.5,
                                    mush_fly_surf.get_height() // 1.5))
                scale_rect = scale.get_rect(center=(700, 465))
                screen.blit(scale, scale_rect)
                pygame.display.update(mush_fly_rect)
                pygame.time.wait(1000)
                return reward_fly_agaric_3
        elif count_achievements() == 200:
            def reward_chanterelles_1():
                mush_chan_surf = pg.image.load('ach_pics/lis.bmp').convert()
                mush_chan_rect = \
                    mush_chan_surf.get_rect(bottomright=(700, 550))
                mush_chan_surf.set_colorkey((0, 0, 0))
                screen.blit(mush_chan_surf, mush_chan_rect)
                pg.display.update()
                return reward_chanterelles_1
        elif count_achievements() == 250:
            def reward_chanterelles_2():
                mush_chan_surf = pg.image.load('ach_pics/lis.bmp').convert()
                mush_chan_rect = \
                    mush_chan_surf.get_rect(bottomright=(700, 550))
                mush_chan_surf.set_colorkey((0, 0, 0))
                screen.blit(mush_chan_surf, mush_chan_rect)
                pg.display.update()

                scale = pygame.transform.scale(
                    mush_chan_surf, (mush_chan_surf.get_width() // 2,
                                     mush_chan_surf.get_height() // 2))
                scale_rect = scale.get_rect(center=(300, 450))
                screen.blit(scale, scale_rect)
                pygame.display.update(mush_chan_rect)
                pygame.time.wait(1000)
                return reward_chanterelles_2
        elif count_achievements() == 300:
            def reward_chanterelles_3():
                mush_chan_surf = pg.image.load('lis.bmp').convert()
                mush_chan_rect = \
                    mush_chan_surf.get_rect(bottomright=(700, 550))
                mush_chan_surf.set_colorkey((0, 0, 0))
                screen.blit(mush_chan_surf, mush_chan_rect)
                pg.display.update()

                scale = pygame.transform.scale(
                    mush_chan_surf, (mush_chan_surf.get_width() // 2,
                                     mush_chan_surf.get_height() // 2))
                scale_rect = scale.get_rect(center=(300, 450))
                screen.blit(scale, scale_rect)
                pygame.display.update(mush_chan_rect)
                pygame.time.wait(1000)

                scale = pygame.transform.scale(
                    mush_chan_surf, (mush_chan_surf.get_width() // 1.5,
                                     mush_chan_surf.get_height() // 1.5))
                scale_rect = scale.get_rect(center=(750, 465))
                screen.blit(scale, scale_rect)
                pygame.display.update(mush_chan_rect)
                pygame.time.wait(1000)
                return reward_chanterelles_3
        elif count_achievements() == 350:
            def reward_white_mush_1():
                mush_white_surf = \
                    pg.image.load('ach_pics/white4.bmp').convert()
                scale = pygame.transform.scale(
                    mush_white_surf, (mush_white_surf.get_width() // 1.5,
                                      mush_white_surf.get_height() // 1.5))
                mush_white_rect = \
                    mush_white_surf.get_rect(bottomright=(870, 700))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_white_rect)
                pg.display.update()
                return reward_white_mush_1
        elif count_achievements() == 400:
            def reward_white_mush_2():
                mush_white_surf = \
                    pg.image.load('ach_pics/white4.bmp').convert()
                scale = pygame.transform.scale(
                    mush_white_surf, (mush_white_surf.get_width() // 1.5,
                                      mush_white_surf.get_height() // 1.5))
                mush_white_rect = \
                    mush_white_surf.get_rect(bottomright=(870, 700))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_white_rect)
                pg.display.update()

                mush_white_surf = \
                    pg.image.load('ach_pics/white4.bmp').convert()
                scale = pygame.transform.scale(
                    mush_white_surf, (mush_white_surf.get_width() // 3,
                                      mush_white_surf.get_height() // 3))
                mush_white_rect = \
                    mush_white_surf.get_rect(bottomright=(690, 900))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_white_rect)
                pg.display.update()
                pygame.time.wait(1000)
                return reward_white_mush_2
        elif count_achievements() == 450:
            def reward_white_mush_3():

                mush_white_surf = \
                    pg.image.load('ach_pics/white4.bmp').convert()
                scale = pygame.transform.scale(
                    mush_white_surf, (mush_white_surf.get_width() // 1.5,
                                      mush_white_surf.get_height() // 1.5))
                mush_white_rect = \
                    mush_white_surf.get_rect(bottomright=(870, 700))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_white_rect)
                pg.display.update()

                mush_white_surf = \
                    pg.image.load('ach_pics/white4.bmp').convert()
                scale = pygame.transform.scale(
                    mush_white_surf, (mush_white_surf.get_width() // 3,
                                      mush_white_surf.get_height() // 3))
                mush_white_rect = \
                    mush_white_surf.get_rect(bottomright=(690, 900))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_white_rect)
                pg.display.update()
                pygame.time.wait(1000)
                mush_white_surf = \
                    pg.image.load('ach_pics/white4.bmp').convert()
                scale = pygame.transform.scale(
                    mush_white_surf, (mush_white_surf.get_width() // 2,
                                      mush_white_surf.get_height() // 2))
                mush_white_rect = \
                    mush_white_surf.get_rect(bottomright=(1200, 850))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_white_rect)
                pg.display.update()
                return reward_white_mush_3
        elif count_achievements() == 500:
            def reward_honey_mush_1():
                mush_honey_surf = \
                    pg.image.load('ach_pics/honeymushrooms.bmp').convert()
                scale = pygame.transform.scale(
                    mush_honey_surf, (mush_honey_surf.get_width() // 2.5,
                                      mush_honey_surf.get_height() // 2.5))
                mush_honey_rect = \
                    mush_honey_surf.get_rect(bottomright=(1400, 1000))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_honey_rect)
                pg.display.update()
                return reward_honey_mush_1
        elif count_achievements() == 550:
            def reward_honey_mush_2():
                mush_honey_surf = \
                    pg.image.load('ach_pics/honeymushrooms.bmp').convert()
                scale = pygame.transform.scale(
                    mush_honey_surf, (mush_honey_surf.get_width() // 2.5,
                                      mush_honey_surf.get_height() // 2.5))
                mush_honey_rect = \
                    mush_honey_surf.get_rect(bottomright=(1400, 1000))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_honey_rect)
                pg.display.update()

                mush_honey_surf = \
                    pg.image.load('ach_pics/honeymushrooms.bmp').convert()
                scale = pygame.transform.scale(
                    mush_honey_surf, (mush_honey_surf.get_width() // 4,
                                      mush_honey_surf.get_height() // 4))
                mush_honey_rect = \
                    mush_honey_surf.get_rect(bottomright=(1200, 1125))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_honey_rect)
                pg.display.update()
                return reward_honey_mush_2
        elif count_achievements() == 600:
            def reward_honey_mush_3():
                mush_honey_surf = \
                    pg.image.load('ach_pics/honeymushrooms.bmp').convert()
                scale = pygame.transform.scale(
                    mush_honey_surf, (mush_honey_surf.get_width() // 2.5,
                                      mush_honey_surf.get_height() // 2.5))
                mush_honey_rect = \
                    mush_honey_surf.get_rect(bottomright=(1400, 1000))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_honey_rect)
                pg.display.update()

                mush_honey_surf = \
                    pg.image.load('ach_pics/honeymushrooms.bmp').convert()
                scale = pygame.transform.scale(
                    mush_honey_surf, (mush_honey_surf.get_width() // 4,
                                      mush_honey_surf.get_height() // 4))
                mush_honey_rect = \
                    mush_honey_surf.get_rect(bottomright=(1200, 1125))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_honey_rect)
                pg.display.update()

                mush_honey_surf = \
                    pg.image.load('ach_pics/honeymushrooms.bmp').convert()
                scale = pygame.transform.scale(
                    mush_honey_surf, (mush_honey_surf.get_width() // 3,
                                      mush_honey_surf.get_height() // 3))
                mush_honey_rect = \
                    mush_honey_surf.get_rect(bottomright=(1700, 1105))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_honey_rect)
                pg.display.update()
                return reward_honey_mush_3
        elif count_achievements() == 650:
            def reward_all():
                mush_honey_surf = \
                    pg.image.load('ach_pics/honeymushrooms.bmp').convert()
                scale = pygame.transform.scale(
                    mush_honey_surf, (mush_honey_surf.get_width() // 4,
                                      mush_honey_surf.get_height() // 4))
                mush_honey_rect = \
                    mush_honey_surf.get_rect(bottomright=(1860, 1145))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_honey_rect)
                pg.display.update()

                mush_white_surf = pg.image.load('ach_pics/white4.bmp').\
                    convert()
                scale = pygame.transform.scale(
                    mush_white_surf, (mush_white_surf.get_width() // 3,
                                      mush_white_surf.get_height() // 3))
                mush_white_rect = \
                    mush_white_surf.get_rect(bottomright=(670, 850))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_white_rect)
                pg.display.update()

                mush_chan_surf = pg.image.load('ach_pics/lis.bmp').convert()
                scale = pygame.transform.scale(
                    mush_chan_surf, (mush_chan_surf.get_width() // 1.3,
                                     mush_chan_surf.get_height() // 1.3))
                mush_chan_rect = \
                    mush_chan_surf.get_rect(bottomright=(580, 680))
                scale.set_colorkey((0, 0, 0))
                screen.blit(scale, mush_chan_rect)
                pg.display.update()

                mush_fly_surf = pg.image.load('ach_pics/mush.bmp').convert()
                mush_fly_rect = mush_fly_surf.get_rect(bottomright=(770, 550))
                mush_fly_surf.set_colorkey((0, 0, 0))
                screen.blit(mush_fly_surf, mush_fly_rect)
                pg.display.update()
                return reward_all
        # и так доделать для остальных, последний случай - >=
        # сколько-то, а не только само это число
        pygame.display.flip()

    def start(self):
        self._set_menu()
        # pygame.display.flip()


class MyGame:
    SIZE = (1000, 600)

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(MyGame.SIZE)
        self.main = MainMenu(self.window)

    def start(self):
        upload_information()
        print('abc')
        self.main.start()


super_deck = []
learned_cards = 0
game = MyGame()
game.start()
