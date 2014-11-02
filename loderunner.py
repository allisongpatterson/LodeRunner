#
# MAZE
# 
# Example game
#
# Version without baddies running around
#


from graphics import *
import random

LEVEL_WIDTH = 35
LEVEL_HEIGHT = 20    

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT

GR_OBS = {'hidden':[]}

BADDIE_DELAY = 1000

def screen_pos (x,y):
    return (x*CELL_SIZE+10,y*CELL_SIZE+10)

def screen_pos_index (index):
    x = index % LEVEL_WIDTH
    y = (index - x) / LEVEL_WIDTH
    return screen_pos(x,y)

def index (x,y):
    return x + (y*LEVEL_WIDTH)

class Queue (object):
    def __init__ (self):
        self._queue = []

    def enqueue (self,delay,obj):
        self._queue.append((delay, obj))
        self._queue.sort()
        # print self._queue

    def dequeue_if_ready (self):
        while self._queue[0][0] == 0:
            evt = self._queue.pop(0)
            evt[1].event(self)
        self._queue = [(x-1,obj) for x,obj in self._queue]


class Hole (object):
    def __init__ (self,x,y,window,level):
        self._x = x
        self._y = y
        self._window = window
        self._level = level

    def event (self,q):        
        sx,sy = screen_pos(self._x,self._y)
        self._level[index(self._x,self._y)] = 1
        GR_OBS[(sx,sy)].draw(self._window)


class Character (object):
    def __init__ (self,pic,x,y,window,level,q):
        (sx,sy) = screen_pos(x,y)
        self._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),pic)
        self._window = window
        self._img.draw(window)
        self._x = x
        self._y = y
        self._level = level
        self._q = q

    def same_loc (self,x,y):
        return (self._x == x and self._y == y)

    def get_surroundings (self):
        up = self._level[index(self._x, self._y-1)]
        down = self._level[index(self._x, self._y+1)]
        left = self._level[index(self._x-1, self._y)]
        right = self._level[index(self._x+1, self._y)]

        return {'u':up, 'd':down, 'l':left, 'r':right}

    def move (self,dx,dy):
        tx = self._x + dx
        ty = self._y + dy
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            old_pos = self._level[index(self._x,self._y)]
            new_pos = self._level[index(tx,ty)]
            if dx:
                if new_pos == 1:
                    return
            if dy == 1:
                if new_pos == 1:
                    return
            if dy == -1:
                if old_pos not in (2,9) or new_pos == 1:
                    return

            while new_pos == 0 and ty < 19 and self._level[index(tx,ty+1)] in (0,3,4):
                ty += 1
                dy += 1
                new_pos = self._level[index(tx,ty)]


            self._x = tx
            self._y = ty
            self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)


class Player (Character):
    def __init__ (self,x,y,window,level,q):
        Character.__init__(self,'t_android.gif',x,y,window,level,q)

    def at_exit (self):
        return (self._y == 0)

    def pickup_gold (self):
        tx = self._x
        ty = self._y
        if self._level[index(tx,ty)] == 4:
            self._level[index(tx,ty)] = 0
            sx, sy = screen_pos(tx,ty)
            GR_OBS[(sx,sy)].undraw()

        if 4 not in self._level:
            for hl in GR_OBS['hidden']:
                hl.undraw()
        
    def make_hole (self, tx, ty):
        self._level[index(tx,ty)] = 0
        sx, sy = screen_pos(tx,ty)
        GR_OBS[(sx,sy)].undraw()

        hole = Hole(tx,ty,self._window,self._level)
        self._q.enqueue(20000,hole)

    def dig (self,dx):
        tx = self._x + dx
        ty = self._y + 1
        if self._level[index(tx,ty)] == 1 and self._level[index(tx,self._y)] == 0:
            self.make_hole(tx,ty)

    def is_crushed (self):
        if self._level[index(self._x,self._y)] == 1:
            lost(self._window)

class Baddie (Character):
    def __init__ (self,x,y,window,level,player,q):
        Character.__init__(self,'t_red.gif',x,y,window,level,q)
        self._player = player

    def event (self,q):
        if self._player.same_loc(self._x,self._y):
            lost(self._window)
        dx,dy = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        self.move(dx,dy)
        q.enqueue(BADDIE_DELAY, self)           

def lost (window):
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU LOST!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)

def won (window):
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU WON!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)



# 0 empty
# 1 brick
# 2 ladder
# 3 rope
# 4 gold
# 9 hidden ladder

def create_level (num):
    screen = [1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,9,
              1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,
              1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,9,
              1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,
              0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,2,1,0,0,0,1,2,0,1,
              0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,1,1,1,1,
              3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,2,0,0,0,0,3,3,3,3,
              2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,
              2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,
              2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,2,1,1,1,1,1,1,1,2,
              2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,
              2,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,
              2,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,2,1,0,0,0,0,3,3,3,2,0,0,1,1,1,1,1,2,
              2,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,2,1,1,1,1,1,1,0,0,2,0,0,1,0,0,0,1,2,
              2,0,1,4,4,1,0,0,1,0,4,4,4,1,0,0,1,2,0,4,4,4,0,1,0,0,2,0,0,1,4,4,4,1,2,
              2,0,1,1,1,1,0,0,1,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,2,0,0,1,1,1,1,1,2,
              2,0,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,2,
              1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,
              1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,1,
              1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    # screen = [1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,9,
    #           1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,
    #           1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,9,
    #           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,
    #           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,2,1,0,0,0,1,2,0,1,
    #           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,1,1,1,1,
    #           3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,2,0,0,0,0,3,3,3,3,
    #           2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,
    #           2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,
    #           2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,2,1,1,1,1,1,1,1,2,
    #           2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,
    #           2,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,
    #           2,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,2,1,0,0,0,0,3,3,3,2,0,0,1,1,1,1,1,2,
    #           2,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,2,1,1,1,1,1,1,0,0,2,0,0,1,0,0,0,1,2,
    #           2,0,1,1,1,1,0,0,1,0,4,4,4,1,0,0,1,2,0,1,1,1,0,1,0,0,2,0,0,1,1,1,1,1,2,
    #           2,0,1,1,1,1,0,0,1,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,2,0,0,1,1,1,1,1,2,
    #           2,0,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,2,
    #           1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,
    #           1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,1,
    #           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    return screen

def create_screen (level,window):

    tiles = {
        1: 'brick.gif',
        2: 'ladder.gif',
        3: 'rope.gif',
        4: 'gold.gif',
        9: 'ladder.gif'
    }

    
    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)

    for (index,cell) in enumerate(level):
        if cell != 0:
            (sx,sy) = screen_pos_index(index)
            elt = image(sx, sy, tiles[cell])
            elt.draw(window)
            GR_OBS[(sx,sy)] = elt
        if cell == 9:
            elt = Rectangle(Point(sx,sy), Point(sx+CELL_SIZE,sy+CELL_SIZE))
            elt.setFill('white')
            elt.setOutline('white')
            elt.draw(window)
            GR_OBS['hidden'].append(elt)


MOVE = {
    'Left': (-1,0),
    'Right': (1,0),
    'Up' : (0,-1),
    'Down' : (0,1)
}
DIG = {
    'z': -1,
    'x': 1
}

def main ():

    window = GraphWin("Maze", WINDOW_WIDTH+20, WINDOW_HEIGHT+20)

    rect = Rectangle(Point(5,5),Point(WINDOW_WIDTH+15,WINDOW_HEIGHT+15))
    rect.setFill('sienna')
    rect.setOutline('sienna')
    rect.draw(window)
    rect = Rectangle(Point(10,10),Point(WINDOW_WIDTH+10,WINDOW_HEIGHT+10))
    rect.setFill('white')
    rect.setOutline('white')
    rect.draw(window)

    level = create_level(1)

    screen = create_screen(level,window)

    q = Queue()

    p = Player(17,18,window,level,q)

    baddie1 = Baddie(5,2,window,level,p,q)
    baddie2 = Baddie(20,2,window,level,p,q)
    baddie3 = Baddie(15,7,window,level,p,q)
    q.enqueue(BADDIE_DELAY, baddie1)
    q.enqueue(BADDIE_DELAY, baddie2)
    q.enqueue(BADDIE_DELAY, baddie3)

    while not p.at_exit():
        key = window.checkKey()
        p.is_crushed()
        if key == 'q':
            window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            p.move(dx,dy)
            p.pickup_gold()
            #p.get_crushed()
        if key in DIG:
            dx = DIG[key]
            p.dig(dx)

        q.dequeue_if_ready()

        # baddies should probably move here

    won(window)

if __name__ == '__main__':
    main()
