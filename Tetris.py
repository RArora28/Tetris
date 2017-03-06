import time
from random import randint
import signal
import sys
import copy

class _GetchUnix:
    def __init__(self):
        import tty, sys 

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch = _GetchUnix()

class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    raise AlarmException

def input_function(timeout=1):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = getch()
        signal.alarm(0)

        return text
    except AlarmException:
        print("\nNo input, Prompt timeout. Continuing...")
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''

class Block :

    def __init__(self, blocks):
        self.blocks = blocks
        
    def check_empty(self, x, y, height, width, board):
        if(x > height-1 or x < 0 or y < 0 or y > width-1):
            return 1
        elif board[x][y] == 'X':
            return 1
        else :
            return 0

    def rotate(self, block, board, height, width) :
        row, col=[],[]
          
        for points in block :
            row.append(points[0])
            col.append(points[1])

        minr = min(row)
        maxr = max(row)
        minc = min(col)
        maxc = max(col)
        temp = [[0 for i in xrange(maxc-minc+1)] for j in xrange(maxr+1-minr)]

        for points in block : 
            x = points[0] - minr
            y = points[1] - minc
            temp[x][y]=1

        new = zip(*temp[::-1])
        check = 0

        for i in xrange(maxr-minr+1):
            for j in xrange(maxc-minc+1):
                if(new[j][i]==1):
                    check+=self.check_empty(minr+j,minc+i, height, width, G.board)
        curr = []
        if(check!=0):
            return curr

        for i in xrange(maxr-minr+1):
            for j in xrange(maxc-minc+1):
                if(new[j][i]==1):
                    curr.append([minr+j,minc+i])
        return curr

    def MoveLeft(self, block, board, height, width):            
        for i in xrange(len(block)):
            if block[i][1] == 1 or board[block[i][0]][block[i][1]-1] == 'X':
                return False
        for i in xrange(len(block)):
            block[i][1] -= 1
        return True
    
    def MoveRight(self, block, board, height, width) :
        for i in xrange(len(block)):
            if block[i][1] == width-2 or board[block[i][0]][block[i][1]+1] == 'X':
                return False
        for i in xrange(len(block)):
            block[i][1] += 1
        return True

    def MoveDown(self, block, board, height, width) :
        for i in xrange(len(block)):
            if block[i][0] == height-2 or board[block[i][0]+1][block[i][1]] == 'X' :
                return True 
        for i in xrange(len(block)):
            block[i][0] += 1
        return False

    def draw(self, block, board, height, width) :
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                if([i,j] in block):
                    print 'X',
                else: 
                    print board[i][j],
            print "\n"
        print "Your Current Score is:", G.score 

    
    def FallDown(self, block, board, height, width) :
        while True:
            for i in xrange(len(block)):
                if block[i][0] == height-2 or board[block[i][0]+1][block[i][1]] == 'X' :
                    return True
            for i in xrange(len(block)):
                block[i][0] += 1


class Board : 
    
    def fillPiecePos(self, block, board):
        for [i,j] in block:
            board[i][j] = 'X'


class GamePlay(Block, Board) :
    
    def __init__(self):
        self.score = 0
        self.board = []
        self.height = 32
        self.width = 30
        self.block = []

        for i in xrange(self.height):
            l , L = [], []
            for j in xrange(self.width):
                if j == 0 or j == (self.width-1):
                    l.append('.')
                else :
                    l.append(' ')
                L.append('.')
            if i == 0 or i == self.height-1:
                self.board.append(L)
            else : 
                self.board.append(l)
     
    def checkRowFull(self, row):
        for i in range(1, len(self.board[0])-2, 1):
            if self.board[row][i] != 'X':
                return False
        return True
        
    def checkRowEmpty(self, row):
        for i in range(1, len(self.board[0])-2, 1):
            if self.board[row][i] == 'X':
                return False
        return True
        
    def updateScore(self, val):
        self.score += val
        
    def selectPiece(self, blocks):
        val = randint(0, 4)
        #val = 0
        self.block = copy.deepcopy(blocks[val])    
        
    def BringDown(self):
        for i in range(self.height-2, 1, -1):
            for j in range(1, len(self.board[0])-1, 1):
                self.board[i][j] = self.board[i-1][j]
        for j in range(1, len(self.block[0])-2, 1):
            self.board[1][j] = ' '

    def Check(self):
        row = self.height-2    
        while True:
            if self.checkRowFull(row):
                self.BringDown()
                self.updateScore(100)
            else:
                return False
    
    def Generate(self, begin, blocks):
        if begin:
            self.selectPiece(blocks)
            begin = False
            
    def cases(self, begin, ch):
        if ch == 'a':
            if begin == False:
                self.MoveLeft(self.block, self.board, self.height, self.width)
        elif ch == 'd':
            if begin == False:
                self.MoveRight(self.block, self.board, self.height, self.width)
        elif ch == ' ':
            begin = self.FallDown(self.block, self.board, self.height, self.width)
        elif ch == 'q':
            sys.exit(0)
        elif(ch=='s'):
            ret = self.rotate(self.block, self.board, self.height, self.width)
            if (len(ret)!=0):
                self.block = []
                self.block = copy.deepcopy(ret)
        if begin:
            self.fillPiecePos(self.block, self.board)
            self.updateScore(10)

    def endCondition(self):
        if self.checkRowEmpty(1) == False:
            print "--------------------------Game Over-----------------------------"
            sys.exit(0)

begin = True #variable to check the generation of new block
blocks=[ [ [1,15],[2,15],[3,15] ,[4,15] ],[ [1,15],[2,15],[1,16],[2,16] ], [ [1,15],[2,15],[2,16],[3,16] ],[ [1,15],[2,15],[3,15],[3,16] ],[ [2,15],[1,16],[2,16],[3,16] ] ]

#Game-Loop

G = GamePlay()
B = Block(blocks)

while True:     
    
    G.Generate(begin, B.blocks)
    B.draw(G.block, G.board, G.height, G.width)
    begin = G.MoveDown(G.block, G.board, G.height, G.width)
    ch = input_function()
    G.cases(begin, ch)
    G.endCondition()
    G.Check()
    
