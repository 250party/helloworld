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
assert RowNumber>1
assert ColNumber>1
BOOMNumber=10           #雷的数目
RectNumber=RowNumber*ColNumber      
RectHeight=36           #包括所有雷的最小面板应该多高
RectWidth=36
RectHeightMiddle=RectHeight//2
RectWidthMiddle=RectWidth//2
RectEdge=1              #雷的边缘美化
RectNumberEdge=4        #数字边缘
NumberThick=3
RectOtherEdge=RectEdge+RectNumberEdge+NumberThick
RectNumberHeight=RectHeight-2*RectOtherEdge
RectNumberWidth=RectWidth-2*RectOtherEdge


assert RectHeight>10     #断言，断定这个成立，否则程序报错
assert RectWidth>10
assert RectHeight>2*RectEdge
assert RectWidth>2*RectEdge
assert RectNumber>BOOMNumber
assert RectOtherEdge*2<RectHeight
assert RectOtherEdge*2<RectWidth

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
ONECOLOR=(65,79,188)
TWOCOLOR=(33,98,1)
THREECOLOR=(168,3,6)
FOURCOLOR=(4,0,124)
FIVECOLOR=(123,1,0)
SIXCOLOR=(28,131,140)
SEVENCOLOR=(159,5,7)
EIGHTCOLOR=(169,9,11)

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
                        Blocks=CalNumber(Blocks)
                        #RevealALL(Blocks)
                    BlockReveal(Blocks,blocky,blockx)
        
        pygame.display.update()
        FPSCLOCK.tick(ScreenFPS)

def CalNumber(Blocks):          #计算格子的数字
    for i in range(ColNumber):
        for j in range(RowNumber):
            if BlockisBOOM(Blocks,i,j): #BOON=-1，以雷来看
                if i!=0 and j!=0:               #左上角
                    if False==BlockisBOOM(Blocks,i-1,j-1):
                        Blocks[i-1][j-1].ChangeContent(+1)
                if i!=0:                        #上方
                    if False==BlockisBOOM(Blocks,i-1,j):
                        Blocks[i-1][j].ChangeContent(+1)
                if i!=0 and j!=RowNumber-1:     #右上角
                    if False==BlockisBOOM(Blocks,i-1,j+1):
                        Blocks[i-1][j+1].ChangeContent(+1)

                if i!=ColNumber-1 and j!=0:       #左下角
                    if False==BlockisBOOM(Blocks,i+1,j-1):
                        Blocks[i+1][j-1].ChangeContent(+1)
                if i!=ColNumber-1:                 #下方
                    if False==BlockisBOOM(Blocks,i+1,j):
                        Blocks[i+1][j].ChangeContent(+1)
                if i!=ColNumber-1 and j!=RowNumber-1:   #右下方
                    if False==BlockisBOOM(Blocks,i+1,j+1):
                        Blocks[i+1][j+1].ChangeContent(+1)

                if j!=0:                            #左边
                    if False==BlockisBOOM(Blocks,i,j-1):
                        Blocks[i][j-1].ChangeContent(+1)
                if j!=RowNumber-1:                  #右边
                    if False==BlockisBOOM(Blocks,i,j+1):
                        Blocks[i][j+1].ChangeContent(+1)
    return Blocks

def BlockisBOOM(Blocks,blocky,blockx):      #这个格子是雷吗
    if Blocks[blocky][blockx].GetContent()==BOOM:
        return True
    else:
        return False

def RevealALL(Blocks):              #揭开所有雷
    for Blockrow in Blocks:
        for anyBlock in Blockrow:
            anyBlock.ChangeVisit(True)

def RandomBOOM(Blocks,blockx,blocky):   #随机赋值雷
    BOOMS=[]
    for i in range(ColNumber*RowNumber-1):  #有一处一定不为雷，在此设置安全区大小
        if i<BOOMNumber:
            BOOMS.append(BOOM)
        else:
            BOOMS.append(0)
    random.shuffle(BOOMS)
    y=0
    for Blockrow in Blocks:             #将包含随机雷的数组赋给Blocks
        x=0
        for anyBlock in Blockrow:
            if x==blockx and y==blocky: #跳过安全区
                pass
            else:
                anyBlock.ChangeContent(BOOMS.pop())
                #print(len(BOOMS))
            x+=1
        y+=1
    return Blocks

def BlockReveal(Blocks,blocky,blockx):      #雷揭开
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

class Line():   #用于格子内图案绘制
    def Middle_UptoDown_Line(x,y,color):    #中竖线
        pygame.draw.line(DISPLAYSURF,color,(x+RectWidthMiddle,y+RectOtherEdge),(x+RectWidthMiddle,y+RectHeight-RectOtherEdge),NumberThick)
    def LefttoRight_Up_Line(x,y,color):     #上横线
        pygame.draw.line(DISPLAYSURF,color,(x+RectOtherEdge,y+RectOtherEdge),(x+RectWidth-RectOtherEdge,y+RectOtherEdge),NumberThick)
    def Left_UptoMiddle_Line(x,y,color):    #左上竖线
        pygame.draw.line(DISPLAYSURF,color,(x+RectOtherEdge,y+RectOtherEdge),(x+RectOtherEdge,y+RectHeightMiddle),NumberThick)
    def Right_UptoMiddle_Line(x,y,color):   #右上竖线
        pygame.draw.line(DISPLAYSURF,color,(x+RectWidth-RectOtherEdge,y+RectOtherEdge),(x+RectWidth-RectOtherEdge,y+RectHeightMiddle),NumberThick)
    def LefttoRight_Middle_Line(x,y,color): #中横线
        pygame.draw.line(DISPLAYSURF,color,(x+RectOtherEdge,y+RectHeightMiddle),(x+RectWidth-RectOtherEdge,y+RectHeightMiddle),NumberThick)
    def Left_MiddletoDown_Line(x,y,color):  #左下竖线
        pygame.draw.line(DISPLAYSURF,color,(x+RectOtherEdge,y+RectHeightMiddle),(x+RectOtherEdge,y+RectHeight-RectOtherEdge),NumberThick)
    def Right_MiddletoDown_Line(x,y,color): #右下竖线
        pygame.draw.line(DISPLAYSURF,color,(x+RectWidth-RectOtherEdge,y+RectHeightMiddle),(x+RectWidth-RectOtherEdge,y+RectHeight-RectOtherEdge),NumberThick)
    def LefttoRight_Down_Line(x,y,color):   #下横线
        pygame.draw.line(DISPLAYSURF,color,(x+RectOtherEdge,y+RectHeight-RectOtherEdge),(x+RectWidth-RectOtherEdge,y+RectHeight-RectOtherEdge),NumberThick)

class Rect(Line):
    def __init__(self):
        self.visit=False
        self.sign=NONE  #空，旗子，问号
        self.content=0  #雷，1，2，3，4，5，6，7，8，9，0
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
    def ChangeContent(self,content):self.content+=content   #这是加号
    def Draw(self):             #绘制图形
        if self.GetVisit()==False:  #如果这个格子没被揭开
            pygame.draw.rect(DISPLAYSURF,LIGHTGREY,(self.Getx()+RectEdge,self.Gety()+RectEdge,RectWidth-RectEdge*2,RectHeight-RectEdge*2),0)
        elif self.GetVisit()==True: #揭开了
            #如果是0123456789雷
            if self.GetContent()==BOOM:
                pygame.draw.rect(DISPLAYSURF,RED,(self.Getx()+RectEdge,self.Gety()+RectEdge,RectWidth-RectEdge*2,RectHeight-RectEdge*2),0)
            elif self.GetContent()==0:
                pass
            elif self.GetContent()==1:
                Line.Middle_UptoDown_Line(self.Getx(),self.Gety(),ONECOLOR)
            elif self.GetContent()==2:  #_|_|_
                Line.LefttoRight_Up_Line(self.Getx(),self.Gety(),TWOCOLOR)
                Line.Right_UptoMiddle_Line(self.Getx(),self.Gety(),TWOCOLOR)
                Line.LefttoRight_Middle_Line(self.Getx(),self.Gety(),TWOCOLOR)
                Line.Left_MiddletoDown_Line(self.Getx(),self.Gety(),TWOCOLOR)
                Line.LefttoRight_Down_Line(self.Getx(),self.Gety(),TWOCOLOR)
            elif self.GetContent()==3:  #_|_|_
                Line.LefttoRight_Up_Line(self.Getx(),self.Gety(),THREECOLOR)
                Line.Right_UptoMiddle_Line(self.Getx(),self.Gety(),THREECOLOR)
                Line.LefttoRight_Middle_Line(self.Getx(),self.Gety(),THREECOLOR)
                Line.Right_MiddletoDown_Line(self.Getx(),self.Gety(),THREECOLOR)
                Line.LefttoRight_Down_Line(self.Getx(),self.Gety(),THREECOLOR)
            elif self.GetContent()==4:  #||_ 
                Line.Left_UptoMiddle_Line(self.Getx(),self.Gety(),FOURCOLOR)
                Line.Middle_UptoDown_Line(self.Getx(),self.Gety(),FOURCOLOR)
                Line.LefttoRight_Middle_Line(self.Getx(),self.Gety(),FOURCOLOR)
            elif self.GetContent()==5:  #_|_|_
                Line.LefttoRight_Up_Line(self.Getx(),self.Gety(),FIVECOLOR)
                Line.Left_UptoMiddle_Line(self.Getx(),self.Gety(),FIVECOLOR)
                Line.LefttoRight_Middle_Line(self.Getx(),self.Gety(),FIVECOLOR)
                Line.Right_MiddletoDown_Line(self.Getx(),self.Gety(),FIVECOLOR)
                Line.LefttoRight_Down_Line(self.Getx(),self.Gety(),FIVECOLOR)
            elif self.GetContent()==6:  #_|_||_
                Line.LefttoRight_Up_Line(self.Getx(),self.Gety(),SIXCOLOR)
                Line.Left_UptoMiddle_Line(self.Getx(),self.Gety(),SIXCOLOR)
                Line.LefttoRight_Middle_Line(self.Getx(),self.Gety(),SIXCOLOR)
                Line.Left_MiddletoDown_Line(self.Getx(),self.Gety(),SIXCOLOR)
                Line.Right_MiddletoDown_Line(self.Getx(),self.Gety(),SIXCOLOR)
                Line.LefttoRight_Down_Line(self.Getx(),self.Gety(),SIXCOLOR)
            elif self.GetContent()==7: #_||
                Line.LefttoRight_Up_Line(self.Getx(),self.Gety(),SEVENCOLOR)
                Line.Right_UptoMiddle_Line(self.Getx(),self.Gety(),SEVENCOLOR)
                Line.Right_MiddletoDown_Line(self.Getx(),self.Gety(),SEVENCOLOR)
            elif self.GetContent()==8: #_||_||_
                Line.LefttoRight_Up_Line(self.Getx(),self.Gety(),EIGHTCOLOR)
                Line.Left_UptoMiddle_Line(self.Getx(),self.Gety(),EIGHTCOLOR)
                Line.Right_UptoMiddle_Line(self.Getx(),self.Gety(),EIGHTCOLOR)
                Line.LefttoRight_Middle_Line(self.Getx(),self.Gety(),EIGHTCOLOR)
                Line.Left_MiddletoDown_Line(self.Getx(),self.Gety(),EIGHTCOLOR)
                Line.Right_MiddletoDown_Line(self.Getx(),self.Gety(),EIGHTCOLOR)
                Line.LefttoRight_Down_Line(self.Getx(),self.Gety(),EIGHTCOLOR)

if __name__=="__main__":
    main()
