#
# MAZE
# 
# Example game
#
# Version without baddies running around
#


from graphics import *

LEVEL_WIDTH = 20
LEVEL_HEIGHT = 20    

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT


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

    def move (self,dx,dy):
        tx = self._x + dx
        ty = self._y + dy
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if self._level[index(tx,ty)] == 0:
                self._x = tx
                self._y = ty
                self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
                

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


def create_level (num):
    screen = []
    screen.extend([1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    screen.extend([1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1])
    screen.extend([1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1])
    screen.extend([1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    screen.extend([1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1])
    screen.extend([1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1])
    screen.extend([1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1])
    screen.extend([1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1])
    screen.extend([1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1])
    screen.extend([1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1])
    screen.extend([1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1])
    screen.extend([1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    screen.extend([1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1])
    screen.extend([1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1])
    screen.extend([1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    return screen

def create_screen (level,window):
    # use this instead of Rectangle below for nicer screen
    brick = 'brick.gif'
    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)

    for (index,cell) in enumerate(level):
        if cell != 0:
            (sx,sy) = screen_pos_index(index)
            elt = Rectangle(Point(sx+1,sy+1),
                            Point(sx+CELL_SIZE-1,sy+CELL_SIZE-1))
            elt.setFill('sienna')
            elt.draw(window)


MOVE = {
    'Left': (-1,0),
    'Right': (1,0),
    'Up' : (0,-1),
    'Down' : (0,1)
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

    p = Player(10,18,window,level)

    baddie1 = Baddie(5,1,window,level,p)
    baddie2 = Baddie(10,1,window,level,p)
    baddie3 = Baddie(15,1,window,level,p)

    while not p.at_exit():
        key = window.checkKey()
        if key == 'q':
            window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            p.move(dx,dy)

        # baddies should probably move here

    won(window)

if __name__ == '__main__':
    main()
