import pygame


class Drawer():
    def __init__(self, window):
        self.window = window
        self.isdestroyed = False

    def _check_quit(self, event):
        if event.type == pygame.QUIT:
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
        self._draw_rect('', (scale[0]+4, scale[1]+4), (pos[0]-2, pos[1]-2), 0, col)
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

class Catalog:
    def __init__(self, name, lang):
        self.name = name
        self.lang = lang

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
    def __draw_catalog_item(self, catalog, pos):
        self._draw_rect('Учить', (50, 25), pos, 14, Clrs.blue)
        self._draw_rect(catalog.name, (700, 25), (pos[0]+52, pos[1]), 16, Clrs.lgray)
        self._draw_image('trashcan.jpg', (25, 25), (pos[0]+754, pos[1]))
        self._draw_image('refresh.png', (25, 25), (pos[0]+781, pos[1]))

    def __add_reverse_catalog(self, i):
        obj = {}
        for j in lst[i].lang:
            obj[lst[i].lang[j]] = j
        lst.append(Catalog(f'{lst[i].name} reversed', obj))

    def _set_menu(self):
        self.window.fill(Clrs.white)
        actions = []
        cnt = 1
        for i in lst:
            self.__draw_catalog_item(i, (100, (cnt)*30))
            actions.append(Square((50, 25), (100, (cnt)*30)))
            actions.append(Square((700, 25), (152, (cnt)*30)))
            actions.append(Square((25, 25), (854, (cnt)*30)))
            actions.append(Square((25, 25), (881, (cnt)*30)))
            cnt+=1
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
                            if act == len(actions)-2:
                                self.isdestroyed = True
                                AddCatalog(self.window).start()
                                break
                            if act == len(actions)-1:
                                self.isdestroyed = True
                                Achievements(self.window).start()
                                break
                            if act%4 == 0:
                                pass # TODO
                            if act%4 == 1:
                                self.isdestroyed = True
                                EditCatalog(self.window).start(act//4)
                                break
                            if act%4 == 2:
                                lst.pop(act//4)
                                self._set_menu()
                            if act%4 == 3:
                                self.__add_reverse_catalog(act//4)
                                actions = self._set_menu()
                            

class AddCatalog(Drawer):
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
                                    lst.append(Catalog(text, {}))
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

class EditCatalog(Drawer):
    def __draw_card(self, i, j, y):
        self._draw_rect(f'{j} - {lst[i].lang[j]}', (500, 50), (235, y), 18, Clrs.lgray)
        self._draw_image('edit.png', (30, 30), (740, y+10))

    def __set_menu(self, ind):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect(f'Редактирование колоды "{lst[ind].name}"', (1000, 20), (0, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        self._draw_image('back.png', (25, 25), (900, 550))
        actions.append(Square((25, 25), (900, 550)))
        self._draw_image('forw.png', (25, 25), (930, 550))
        actions.append(Square((25, 25), (930, 550)))
        self._draw_image('plus.png', (50, 50), (475, 540))
        actions.append(Square((50, 50), (475, 540)))
        cnt = 1
        for j in list(lst[ind].lang.keys())[self.offset:self.offset+8]:
            y = 60*cnt
            self.__draw_card(ind, j, y)
            actions.append(Square((40, 40), (740, y+5)))
            cnt+=1
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
                                k = list(lst[ind].lang.keys())[act-4]
                                EditCard(self.window).start(ind, k)
                                break
                            if act == 0:
                                self.isdestroyed = True
                                MainMenu(self.window).start()
                                break
                            if act == 1:
                                self.offset = max(0, self.offset-8)
                                page = max(0, page-1)
                                self.__set_menu(ind)
                            if act == 2:
                                if self.offset+8 < len(lst[ind].lang):
                                    self.offset = min(len(lst[ind].lang), self.offset+8)
                                    page+=1
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
        text = [word, lst[ind].lang[word]]
        self._draw_input((400, 50), (300, 200), text[0], isclicked[0])
        actions.append(Square((400, 50), (300, 200)))
        self._draw_input((400, 50), (300, 300), text[1], isclicked[1])
        actions.append(Square((400, 50), (300, 300)))
        pygame.display.update()
        return actions

    def start(self, ind, word):
        actions = self._set_menu(ind, word)
        text = [word, lst[ind].lang[word]]
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
                                EditCatalog(self.window).start(ind)
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
                                EditCatalog(self.window).start(ind)
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

class Achievements(Drawer):
    def _set_menu(self):
        self.window.fill(Clrs.white)
        # TODO
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
                
lst = [Catalog('Колода тест 1', {'мем': 'mem'}), Catalog('Колода тест 2', {'test': 'тест', 'something': 'что-то', 'I': 'я', 'I1': 'я1', 'I2': 'я2', 'I3': 'я3', 'I4': 'я4', 'I5': 'я5', 'I6': 'я6', 'I7': 'я7'}), Catalog('Колода тест 3', {'another': 'другой'})]
game = MyGame()
game.start()

