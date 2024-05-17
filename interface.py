import pygame


class Drawer():
    def __init__(self, window):
        self.window = window

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

class MainMenu(Drawer):
    def __draw_catalog_item(self, catalog, pos):
        self._draw_rect('Учить', (50, 25), pos, 14, Clrs.blue)
        self._draw_rect(catalog.name, (700, 25), (pos[0]+52, pos[1]), 16, Clrs.lgray)
        self._draw_image('trashcan.jpg', (25, 25), (pos[0]+754, pos[1]))
        self._draw_image('refresh.png', (25, 25), (pos[0]+781, pos[1]))

    def __add_reverse_catalog(self, i):
        obj = {}
        for j in lst[i].lang:
            obj[lst[i].lang[j]] = i
        lst.append(Catalog(f'{lst[i].name} reversed', obj))
    
    def start(self):
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
        self._draw_rect('Добавить', (MyGame.SIZE[0], 50), (0, MyGame.SIZE[1]-50), 18, Clrs.white)
        actions.append(Square((MyGame.SIZE[0], 50), (0, MyGame.SIZE[1]-50)))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.x1 <= x <= i.x2 and \
                           i.y1 <= y <= i.y2:
                            if act == len(actions)-1:
                                AddCatalog(self.window).start()
                                break
                            if act%4 == 0:
                                pass
                            if act%4 == 1:
                                EditCatalog(self.window).start(act//4)
                            if act%4 == 2:
                                lst.pop(act//4)
                                self.start()
                                break
                            if act%4 == 3:
                                self.__add_reverse_catalog(act//4)
                                self.start()
                                break


class AddCatalog(Drawer):
    def _update_input(self, text, isclicked):
        col = Clrs.black if isclicked else Clrs.white
        self._draw_rect('', (404, 54), (298, 198), 0, col)
        self._draw_rect(text, (400, 50), (300, 200), 20, Clrs.lgray)
    
    def start(self):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect('Создание колоды', (200, 20), (400, 20), 24, Clrs.white)
        isclicked = False
        text = ''
        self._update_input(text, isclicked)
        actions.append(Square((400, 50), (300, 200)))
        self._draw_rect('Сохранить', (300, 50), (350, 500), 18, Clrs.white)
        actions.append(Square((300, 50), (350, 500)))
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isclicked = False
                    x, y = event.pos
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.x1 <= x <= i.x2 and \
                           i.y1 <= y <= i.y2:
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                self._update_input(text, isclicked)
                pygame.display.update()

class EditCatalog(Drawer):
    def start(self, ind):
        self.window.fill(Clrs.white)
        actions = []
        self._draw_rect('Редактирование колоды', (200, 20), (400, 20), 24, Clrs.white)
        self._draw_image('back.png', (25, 25), (18, 18))
        actions.append(Square((25, 25), (18, 18)))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                self._check_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isclicked = False
                    x, y = event.pos
                    for act in range(len(actions)):
                        i = actions[act]
                        if i.x1 <= x <= i.x2 and \
                           i.y1 <= y <= i.y2:
                            if act == 0:
                                MainMenu(self.window).start()
                                break

class MyGame:
    SIZE = (1000, 600)

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(MyGame.SIZE)
        self.main = MainMenu(self.window)

    def start(self):
        self.main.start()
                
lst = [Catalog('Колода тест 1', {'мем': 'mem'}), Catalog('Колода тест 2', {'test': 'тест', 'something': 'что-то', 'I': 'я'}), Catalog('Колода тест 3', {'another': 'другой'})]
game = MyGame()
game.start()

