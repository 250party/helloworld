import pygame,sys
from pygame.locals import *
import random

FLAG="flag"
MISTERY="mistery"
NONE="none"

BOOM=-1

ScreenFPS=30
RowNumber=9
ColNumber=9
BOOMNumber=10
RectNumber=RowNumber*ColNumber      
RectHeight=36
RectWidth=36
RectEdge=1
assert RectHeight>2
assert RectWidth>2
assert RectHeight>2*RectEdge
assert RectWidth>2*RectEdge
assert RectNumber>BOOMNumber

ButtonHeight=20
EdgeHeight=EdgeWidth=6
FuncHeight=48

OthersHeight=ButtonHeight+EdgeHeight+FuncHeight+EdgeHeight
ScreenHeight=OthersHeight+RectHeight*ColNumber+EdgeHeight
ScreenWidth=EdgeWidth+RectWidth*RowNumber+EdgeWidth

WHITE=(255,255,255)
RED=(255,0,0)
LIGHTGREY=(224,224,224)
BLACK=(0,0,0)

def main():
    global DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((ScreenWidth,ScreenHeight))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('minesweeper')

    Blocks=InitBoard()

    mousex=0
    mousey=0
    FirstClick=False
    while True:
        DISPLAYSURF.fill(WHITE)
        DrawScreen(Blocks)

        mouseLeftClicked=False
        mouseRightClicked=False

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button==1:
                    mouseLeftClicked=True
                elif event.button==3:
                    mouseRightClicked=True
                mousex, mousey = event.pos

            blockx,blocky= whatBlock(mousex,mousey)
            if (mouseLeftClicked or mouseRightClicked) and ClickBoard(mousex,mousey):
                if mouseLeftClicked:
                    if FirstClick==False:
                        FirstClick=True
                        Blocks=RandomBOOM(Blocks,blockx,blocky)
                        #RevealALL(Blocks)
                    BlockReveal(Blocks,blockx,blocky)
        
        pygame.display.update()
        FPSCLOCK.tick(ScreenFPS)

def RevealALL(Blocks):
    for Blockrow in Blocks:
        for anyBlock in Blockrow:
            anyBlock.ChangeVisit(True)

def RandomBOOM(Blocks,blockx,blocky):
    BOOMS=[]
    for i in range(ColNumber*RowNumber-1):
        if i<BOOMNumber:
            BOOMS.append(BOOM)
        else:
            BOOMS.append(0)
    random.shuffle(BOOMS)
    y=0
    for Blockrow in Blocks:
        x=0
        for anyBlock in Blockrow:
            if x==blockx and y==blocky:
                pass
            else:
                anyBlock.ChangeContent(BOOMS.pop())
                print(len(BOOMS))
            x+=1
        y+=1
    print(len(BOOMS))
    return Blocks

            
def BlockReveal(Blocks,blockx,blocky):
    Blocks[blocky][blockx].ChangeVisit(True)
    
def whatBlock(mousex,mousey):   #不要随意等于，不然就把None检测考虑进去
    if mousey<OthersHeight or mousey>OthersHeight+ColNumber*RectHeight:
        return (None,None)
    elif mousex<EdgeWidth or mousex>EdgeWidth+RowNumber*RectWidth:
        return (None,None)
    else:
        blockx=(mousex-EdgeWidth)//RectWidth
        blocky=(mousey-OthersHeight)//RectHeight
        return(blockx,blocky)
    
def ClickBoard(mousex,mousey):
    Crect=pygame.Rect(EdgeWidth,OthersHeight,RowNumber*RectWidth ,ColNumber*RectHeight)
    if Crect.collidepoint(mousex,mousey):
        return True
    else:
        return False
    
def InitBoard():
    Blocks=[]
    for i in range(ColNumber):
        BlocksRow=[]
        for j in range(RowNumber):
            anyBlock=Rect()
            anyBlock.ChangePos(EdgeWidth+RectWidth*j,OthersHeight+RectHeight*i)
            BlocksRow.append(anyBlock)
        Blocks.append(BlocksRow)
    return Blocks

def DrawScreen(Blocks):
    DrawButtonLine()
    for Blockrow in Blocks:
        for anyBlock in Blockrow:
            anyBlock.Draw()

def DrawButtonLine():
    pygame.draw.rect(DISPLAYSURF,LIGHTGREY,(0,0,ScreenWidth,ButtonHeight))
    #pygame.draw.line(DISPLAYSURF,BLACK,(0,OthersHeight-1),(ScreenWidth//2,OthersHeight),1) #位置测试

class Rect():
    def __init__(self):
        self.visit=False
        self.sign=NONE
        self.content=0
        self.posx=0     #左上角
        self.posy=0

    def GetVisit(self):return self.visit
    def GetSign(self):return self.sign
    def GetContent(self):return self.content
    def Getx(self):return self.posx
    def Gety(self):return self.posy

    def ChangePos(self,posx,posy):
        self.posx=posx
        self.posy=posy
    def ChangeVisit(self,status):self.visit=status
    def ChangeSign(self,sign):self.sign=sign
    def ChangeContent(self,content):self.content=content
    def Draw(self):
        if self.GetVisit()==False:
            pygame.draw.rect(DISPLAYSURF,LIGHTGREY,(self.Getx()+RectEdge,self.Gety()+RectEdge,RectWidth-RectEdge*2,RectHeight-RectEdge*2),0)
        elif self.GetVisit()==True:
            if self.GetContent()==BOOM:
                pygame.draw.rect(DISPLAYSURF,RED,(self.Getx()+RectEdge,self.Gety()+RectEdge,RectWidth-RectEdge*2,RectHeight-RectEdge*2),0)
            
    
if __name__=="__main__":
    main()
