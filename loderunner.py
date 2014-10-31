#
# MAZE
# 
# Example game
#
# Version without baddies running around
#


from graphics import *

LEVEL_WIDTH = 35
LEVEL_HEIGHT = 20    

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT

GR_OBS = {}

def screen_pos (x,y):
    return (x*CELL_SIZE+10,y*CELL_SIZE+10)

def screen_pos_index (index):
    x = index % LEVEL_WIDTH
    y = (index - x) / LEVEL_WIDTH
    return screen_pos(x,y)

def index (x,y):
    return x + (y*LEVEL_WIDTH)

class Character (object):
    def __init__ (self,pic,x,y,window,level):
        (sx,sy) = screen_pos(x,y)
        self._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),pic)
        self._window = window
        self._img.draw(window)
        self._x = x
        self._y = y
        self._level = level

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
                if old_pos != 2 or new_pos == 1:
                    return

            while new_pos == 0 and self._level[index(tx,ty+1)] in [0,3,4]:
                ty += 1
                dy += 1
                new_pos = self._level[index(tx,ty)]

            if new_pos == 4:
                self._level[index(tx,ty)] = 0
                sx, sy = screen_pos(tx,ty)
                GR_OBS[(sx,sy)].undraw()
                gold_gone(self._level,self._window)
                
            self._x = tx
            self._y = ty
            self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
        has_win(self._x,self._y,self._level,self._window)

    def make_hole (self, tx, ty):
        self._level[index(tx,ty)] = 0
        sx, sy = screen_pos(tx,ty)
        GR_OBS[(sx,sy)].undraw()

    def dig (self,dx):
        tx = self._x + dx
        ty = self._y + 1
        if self._level[index(tx,ty)] == 1 and self._level[index(tx,self._y)] == 0:
            self.make_hole(tx,ty)


def gold_gone(level,window):
    if 4 not in level:
        win_ladder(level,window)
    # else:
    #     print 'still gold left'

def win_ladder(level,window):
    tiles = {
            1: 'brick.gif',
            2: 'ladder.gif',
            3: 'rope.gif',
            4: 'gold.gif'
            }

    x = 34
    level[index(x,0)] = 2
    a,b = screen_pos(x,0)
    elt1 = Image(Point(a+CELL_SIZE/2,b+CELL_SIZE/2),tiles[2])
    elt1.draw(window)

    level[index(x,1)] = 2
    c,d = screen_pos(x,1)
    elt2 = Image(Point(c+CELL_SIZE/2,d+CELL_SIZE/2),tiles[2])
    elt2.draw(window)

    level[index(x,2)] = 2
    e,f = screen_pos(x,2)
    elt3 = Image(Point(e+CELL_SIZE/2,f+CELL_SIZE/2),tiles[2])
    elt3.draw(window)

def has_win(x,y,level,window):
    if x == 34 and y == 0:
        won(window)
    

class Player (Character):
    def __init__ (self,x,y,window,level):
        Character.__init__(self,'android.gif',x,y,window,level)

    def at_exit (self):
        return (self._y == 0)


class Baddie (Character):
    def __init__ (self,x,y,window,level,player):
        Character.__init__(self,'red.gif',x,y,window,level)
        self._player = player


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

def create_level (num):
    screen = [1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,0,
              1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
              1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,
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

    # screen = [1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,0,
    #           1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    #           1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,
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
        4: 'gold.gif'
    }

    
    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)

    for (index,cell) in enumerate(level):
        if cell != 0:
            (sx,sy) = screen_pos_index(index)
            elt = image(sx, sy, tiles[cell])
            elt.draw(window)
            GR_OBS[(sx,sy)] = elt


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

    p = Player(17,18,window,level)

    # baddie1 = Baddie(5,1,window,level,p)
    # baddie2 = Baddie(10,1,window,level,p)
    # baddie3 = Baddie(15,1,window,level,p)

    while not p.at_exit():
        key = window.checkKey()
        if key == 'q':
            window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            p.move(dx,dy)
        if key in DIG:
            dx = DIG[key]
            p.dig(dx)

        # baddies should probably move here

    won(window)

if __name__ == '__main__':
    main()
