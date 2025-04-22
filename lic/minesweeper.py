import pygame,sys
from pygame.locals import *
import random

FLAG="flag"
MISTERY="mistery"
NONE="none"

BOOM=-1

ScreenFPS=30            #刷新率
RowNumber=9             #一行有多少格子
ColNumber=9     
BOOMNumber=10           #雷的数目
RectNumber=RowNumber*ColNumber      
RectHeight=36           #包括所有雷的最小面板应该多高
RectWidth=36
RectEdge=1              #雷的边缘美化
assert RectHeight>2     #断言，断定这个成立，否则程序报错
assert RectWidth>2
assert RectHeight>2*RectEdge
assert RectWidth>2*RectEdge
assert RectNumber>BOOMNumber

ButtonHeight=20         #预留按钮高度
EdgeHeight=EdgeWidth=6  #面板间边界美化
FuncHeight=48           #计时，剩余雷数，重来预留高度

OthersHeight=ButtonHeight+EdgeHeight+FuncHeight+EdgeHeight  #你也不想写一大串吧
ScreenHeight=OthersHeight+RectHeight*ColNumber+EdgeHeight   #屏幕高度
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

def RevealALL(Blocks):              #揭开所有雷
    for Blockrow in Blocks:
        for anyBlock in Blockrow:
            anyBlock.ChangeVisit(True)

def RandomBOOM(Blocks,blockx,blocky):   #随机赋值雷
    BOOMS=[]
    for i in range(ColNumber*RowNumber-1):  #有一处一定不为雷
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

def BlockReveal(Blocks,blockx,blocky):      #雷揭开
    Blocks[blocky][blockx].ChangeVisit(True)
    
def whatBlock(mousex,mousey):   #将鼠标位置转为雷的位置
    if mousey<OthersHeight or mousey>OthersHeight+ColNumber*RectHeight:  #不要随意等于，不然就把None检测考虑进去   
        return (None,None)
    elif mousex<EdgeWidth or mousex>EdgeWidth+RowNumber*RectWidth:
        return (None,None)
    else:
        blockx=(mousex-EdgeWidth)//RectWidth
        blocky=(mousey-OthersHeight)//RectHeight
        return(blockx,blocky)
    
def ClickBoard(mousex,mousey):      #检测是否点击扫雷面板
    Crect=pygame.Rect(EdgeWidth,OthersHeight,RowNumber*RectWidth ,ColNumber*RectHeight)
    if Crect.collidepoint(mousex,mousey):
        return True
    else:
        return False
    
def InitBoard():        #初始化数据
    Blocks=[]
    for i in range(ColNumber):
        BlocksRow=[]
        for j in range(RowNumber):
            anyBlock=Rect()
            anyBlock.ChangePos(EdgeWidth+RectWidth*j,OthersHeight+RectHeight*i)
            BlocksRow.append(anyBlock)
        Blocks.append(BlocksRow)
    return Blocks

def DrawScreen(Blocks):     #UI
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
