import random, time, pygame, sys
from pygame.locals import *
fps = 25
windowwidth = 640 
windowheight = 480  
boxsize = 20        
boardwidth = 10   
boardheight = 20
blank = '.'
moveside_freq = 0.15
movedown_freq = 0.00001

l_rmargin = int((windowwidth - (boardwidth*boxsize)) / 2)
topmargin = windowheight - (boardheight*boxsize) - 5

white= (255,255,255)
black= (0,0,0)
gray= (185,185,185)
red= (155,0,0)
lightred= (175,20,20)
green= (0,155,0)
lightgreen= (20,175,20)
blue= (0,0,155)
lightblue= (20,20,175)
yellow= (155,155,0)
lightyellow= (175,175,20)

border= white
bgcolor= black
textcolor= white
shadowcolor=gray
colors=(red,green,blue,yellow)
lightcolors=(lightred,lightgreen,lightblue,lightyellow)
assert len(colors) == len(lightcolors)

template_h=template_w=5
S_template=[['.....',
             '.....',
             '..00.',
             '.00..',
             '.....'],
            ['.....',
             '..0..',
             '..00.',
             '...0.',
             '.....']
            ]
Z_template=[['.....',
             '.....',
             '.00..',
             '..00.',
             '.....'],
            ['.....',
             '..0..',
             '.00..',
             '.0...',
             '.....']]
T_template=[['.....',
             '..0..',
             '.000.',
             '.....',
             '.....'],
            ['.....',
             '..0..',
             '.00..',
             '..0..',
             '.....'],
            ['.....',
             '.....',
             '.000.',
             '..0..',
             '.....'],
            ['.....',
             '..0..',
             '..00.',
             '..0..',
             '.....']]
I_template=[['..0..',
             '..0..',
             '..0..',
             '..0..',
             '.....'],
            ['.....',
             '.....',
             '0000.',
             '.....',
             '.....']]
O_template=[['.....',
             '.....',
             '.00..',
             '.00..',
             '.....']]
L_template=[['.....',
             '..0..',
             '..0..',
             '..00.',
             '.....'],
            ['.....',
             '.00..',
             '..0..',
             '..0..',
             '.....'],
            ['.....',
             '...0.',
             '.000.',
             '.....',
             '.....'],
            ['.....',
             '.....',
             '.000.',
             '.0...',
             '.....']]
J_template=[['.....',
             '..0..',
             '..0..',
             '.00..',
             '.....'],
            ['.....',
             '..00.',
             '..0..',
             '..0..',
             '.....'],
            ['.....',
             '.....',
             '.000.',
             '...0.',
             '.....'],
            ['.....',
             '.0...',
             '.000.',
             '.....',
             '.....']]
shapes= {
        'I': I_template,
        'J': J_template,
        'L': L_template,
        'O': O_template,
        'S': S_template,
        'T': T_template,
        'Z': Z_template }

def main():
    global fpsclock, displaysurf, basicfont,bigfont
    pygame.init()
    fpsclock=pygame.time.Clock()
    displaysurf=pygame.display.set_mode((windowwidth,windowheight))
    basicfont=pygame.font.SysFont('arial.tff',18)
    bigfont=pygame.font.SysFont('freesansbold.tff',100)
    pygame.display.set_caption("Tetromino")

    showtextscreen('Tetromino')
    while True:
        rungame()
        showtextscreen('Game Over')

def rungame():
    board=getblankboard()
    lastmovedown=time.time()
    lastmoveside=time.time()
    lastfall=time.time()
    down=False
    left=False
    right=False
    score=0
    level, fallfreq = calclevelandfallfreq(score)
    fallpiece=getnewpiece()
    nextpiece=getnewpiece()
    while True:
        if fallpiece==None:
            fallpiece=nextpiece
            nextpiece=getnewpiece()
            lastfall=time.time()
            if not isvalidpos(board,fallpiece):
                return
        checkforquit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_p :
                    displaysurf.fill(bgcolor)
                    pygame.mixer.music.stop()
                    showtextscreen('Paused')
                    pygame.mixer.music.play(-1,0.0)
                    lastfall=time.time()
                    lastmovedown=time.time()
                    lastmoveside=time.time()
                elif (event.key==K_LEFT or event.key==K_a):
                    left=False
                elif (event.key==K_RIGHT or event.key==K_d):
                    right=False
                elif (event.key==K_DOWN or event.key==K_s):
                    down=False
            elif event.type==KEYDOWN:
                if(event.key==K_LEFT or event.key==K_a) and isvalidpos(board,fallpiece,adjX=-1):
                    fallpiece['x']-=1
                    left=True
                    right=False
                    lastmoveside=time.time()
                elif(event.key==K_RIGHT or event.key==K_d) and isvalidpos(board,fallpiece,adjX=1):
                    fallpiece['x']+=1
                    left=False
                    right=True
                    lastmoveside=time.time()
                elif (event.key==K_UP or event.key==K_w):
                    fallpiece['rotation']=(fallpiece['rotation']+1)%len(shapes[fallpiece['shape']])
                    if not isvalidpos(board,fallpiece):
                        fallpiece['rotation']=(fallpiece['rotation']-1)%len(shapes[fallpiece['shape']])
                elif(event.key==K_q):
                    fallpiece['rotation']=(fallpiece['rotation']-1)&len(shapes[fallpiece['shape']])
                    if not isvalidpos(board,fallpiece):
                        fallpiece['rotation']=(fallpiece['rotation']+1)%len(shapes[fallpiece['shape']])
                elif(event.key==K_DOWN or event.key==K_s):
                    down=True
                    if isvalidpos(board,fallpiece,adjY=1):
                        fallpiece['y']+=1
                    lastmovedown=time.time()
                elif(event.key==K_SPACE):
                    down=False
                    left=False
                    right=False
                    for i in range (1,boardheight):
                        if not isvalidpos(board,fallpiece,adjY=i):
                            break
                    fallpiece['y']+=i-1
        if((left or right) and (time.time()-lastmoveside)>moveside_freq):
            if left and isvalidpos(board,fallpiece,adjX=-1):
                fallpiece['x']-=1
            elif right and isvalidpos(board,fallpiece,adjX=1):
                fallpiece['x']+=1
            lastmoveside=time.time()
        if(down and (time.time()-lastmovedown)>movedown_freq and isvalidpos(board,fallpiece,adjY=1)):
            fallpiece['y']+=1
            lastmovedown=time.time()
        if ((time.time()-lastfall)>fallfreq):
            if not isvalidpos(board,fallpiece,adjY=1):
                addtoboard(board,fallpiece)
                score+=removecomplines(board)
                level,fallfreq=calclevelandfallfreq(score)
                fallpiece=None
            else:
                fallpiece['y']+=1 
                lastfall=time.time()
        displaysurf.fill(bgcolor)
        drawboard(board)
        drawstatus(score,level)
        drawnextpiece(nextpiece)
        if fallpiece!=None:
            drawpiece(fallpiece)
        pygame.display.update()
        fpsclock.tick(fps)

def maketextobj(text,font,color):
    surf=font.render(text,True,color)
    return surf,surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def getnewpiece():
    shape=random.choice(list(shapes.keys()))
    newpiece={'shape': shape,
              'rotation': random.randint(0,len(shapes[shape])-1),
              'x': int(boardwidth/2)-int(template_w/2),
              'y': -2,
              'color': random.randint(0,len(colors)-1)  }
    return newpiece

def isonboard(x,y):
    return x>=0 and x<boardwidth and y<boardheight

def isvalidpos(board,piece,adjX=0,adjY=0):
    for x in range(template_w):
        for y in range(template_h):
            isaboveboard=(y+piece['y']+adjY) < 0
            if isaboveboard or shapes[piece['shape']][piece['rotation']][y][x]==blank:
                continue
            if not isonboard(x+piece['x']+adjX,y+piece['y']+adjY):
                return False
            if board[x+piece['x']+adjX][y+piece['y']+adjY] != blank:
                return False
    return True

def iscompline(board,y):
    for x in range(boardwidth):
        if board[x][y]==blank:
            return False
    return True

def getblankboard():
    board=[]
    for i in range(boardwidth):
        board.append([blank]*boardheight)
    return board

def calclevelandfallfreq(score):
    level=int(score/10)+1
    fallfreq=0.27-(level*0.2)
    return level,fallfreq

def checkforkeypress():
    checkforquit()
    for event in pygame.event.get([KEYDOWN,KEYUP]):
        if event.type==KEYDOWN:
            continue
        return event.key
    return None

def checkforquit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key==K_ESCAPE:
            terminate()
        pygame.event.post(event)

def addtoboard(board,piece):
    for x in range(template_w):
        for y in range(template_h):
            if shapes[piece['shape']][piece['rotation']][y][x]!=blank:
                board[x+piece['x']][y+piece['y']]=piece['color']

def drawnextpiece(piece):
    nextsurf=basicfont.render('Next: ',True,textcolor)
    nextrect=nextsurf.get_rect()
    nextrect.topleft=(windowwidth-120,80)
    displaysurf.blit(nextsurf,nextrect)
    drawpiece(piece,pixelx=windowwidth-120,pixely=100)

def drawpiece(piece, pixelx=None, pixely=None): 
    shapetodraw = shapes[piece['shape']][piece['rotation']] 
    if pixelx == None and pixely == None: 
        pixelx, pixely = converttopixelcoords(piece['x'], piece['y']) 
  
    for x in range(template_w): 
        for y in range(template_h): 
            if shapetodraw[y][x] != blank: 
                drawbox(None, None, piece['color'], pixelx + (x * 
boxsize), pixely + (y * boxsize)) 
                
def converttopixelcoords(boxx, boxy): 
    return (l_rmargin + (boxx * boxsize)), (topmargin + (boxy * boxsize)) 

def drawboard(board): 
    pygame.draw.rect(displaysurf, border, (l_rmargin - 3, topmargin - 7, (boardwidth * boxsize) + 8, (boardheight * boxsize) + 8), 5)
    pygame.draw.rect(displaysurf, bgcolor, (l_rmargin, topmargin, boxsize * boardwidth, boxsize * boardheight)) 
    for x in range(boardwidth): 
        for y in range(boardheight): 
            drawbox(x, y, board[x][y])

def drawstatus(score, level): 
    scoresurf = basicfont.render('Score: %s' % score, True, textcolor) 
    scorerect = scoresurf.get_rect() 
    scorerect.topleft = (windowwidth - 150, 20) 
    displaysurf.blit(scoresurf, scorerect)
    levelsurf = basicfont.render('Level: %s' % level, True, textcolor) 
    levelrect = levelsurf.get_rect() 
    levelrect.topleft = (windowwidth - 150, 50) 
    displaysurf.blit(levelsurf, levelrect) 

def drawbox(boxx, boxy, color, pixelx=None, pixely=None): 
    if color == blank: 
        return 
    if pixelx == None and pixely == None: 
        pixelx, pixely = converttopixelcoords(boxx, boxy) 
    pygame.draw.rect(displaysurf, colors[color], (pixelx + 1, pixely + 1, boxsize - 1, boxsize - 1)) 
    pygame.draw.rect(displaysurf, lightcolors[color], (pixelx + 1, pixely + 1, boxsize - 4, boxsize - 4)) 

def removecomplines(board): 
    linesremoved = 0 
    y = boardheight - 1
    while y >= 0: 
        if iscompline(board, y): 
            for pulldownY in range(y, 0, -1): 
                for x in range(boardwidth): 
                    board[x][pulldownY] = board[x][pulldownY-1] 
            for x in range(boardwidth): 
                board[x][0] = blank 
            linesremoved += 1
        else: 
            y -= 1 
    return linesremoved 

def showtextscreen(text):  
    titlesurf, titlerect = maketextobj(text, bigfont, shadowcolor) 
    titlerect.center = (int(windowwidth / 2), int(windowheight / 2)) 
    displaysurf.blit(titlesurf, titlerect) 
 
    titlesurf, titlerect = maketextobj(text, bigfont, textcolor)
    titlerect.center = (int(windowwidth / 2) - 3, int(windowheight / 2) - 3) 
    displaysurf.blit(titlesurf, titlerect) 
 
    presskeysurf, presskeyrect = maketextobj('Press a key to play.', basicfont, textcolor) 
    presskeyrect.center = (int(windowwidth / 2), int(windowheight / 2) + 100) 
    displaysurf.blit(presskeysurf, presskeyrect) 
 
    while checkforkeypress() == None: 
        pygame.display.update() 
        fpsclock.tick()

if __name__=='__main__':
    main()