import pygame,sys
from pygame.locals import *
import random
from time import *

FLAG="flag"
MISTERY="mistery"
NONE="none"

BOOM=-1

ScreenFPS=30            #刷新率
RowNumber=9             #一列有多少格子
ColNumber=9     
assert RowNumber>1
assert ColNumber>1

BOOMNumber=10           #雷的数目
RectNumber=RowNumber*ColNumber    
assert RectNumber>BOOMNumber

RectHeight=36           #格子高度
RectWidth=36
assert RectHeight>10     #断言，断定这个成立，否则程序报错
assert RectWidth>10

RectHeightMiddle=RectHeight//2
RectWidthMiddle=RectWidth//2

RectEdge=1
RectShadowEdge=2        #格子边缘预留
NumberHeightExpand=0.8  #数字占格子的高度比例
NumberWidthExpand=0.5
RectNumberHeight=RectHeight*NumberHeightExpand  #数字高
RectNumberWidth=RectWidth*NumberWidthExpand
RectNumbery=(RectHeight*(1-NumberHeightExpand))//2  #数字与格子左上角的相对高度
RectNumberx=(RectWidth*(1-NumberWidthExpand))//2

assert RectEdge<RectHeight
assert RectEdge<RectWidth
assert RectNumberHeight<RectHeight
assert RectNumberWidth<RectWidth
assert RectShadowEdge<RectHeight
assert RectShadowEdge<RectWidth

ButtonHeight=20         #预留按钮高度
EdgeHeight=EdgeWidth=6  #面板间边界美化
FuncHeight=48           #计时，剩余雷数，重来预留高度

OthersHeight=ButtonHeight+EdgeHeight+FuncHeight+EdgeHeight  #你也不想写一大串吧
ScreenHeight=OthersHeight+RectHeight*ColNumber+EdgeHeight   #屏幕高度
ScreenWidth=EdgeWidth+RectWidth*RowNumber+EdgeWidth

TimePosx=ScreenWidth*2//3
BoomNumberPosy=TimePosy=ButtonHeight+FuncHeight//3

BoomNumberHeight=TimeHeight=FuncHeight*2//3
TimeWidth=FuncHeight

BoomNumberPosx=ScreenWidth//4
BoomNumberWidth=FuncHeight*2//3

assert TimeWidth<ScreenWidth//3
assert BoomNumberWidth<ScreenWidth//2-BoomNumberPosx

WHITE=(255,255,255)
RED=(255,0,0)
DARKRED=(176,7,14)
SILVERCOLOR=(192,192,192)
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
    startTime=0
    startTimeFlag=False
    alreadytime=0
    boomnumber_screen=boomnumber=BOOMNumber
    while True:
        DISPLAYSURF.fill(WHITE)
        DrawScreen(Blocks,alreadytime,boomnumber_screen)

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
 
            blockx,blocky= whatBlock(mousex,mousey)         #将鼠标位置转为雷的位置
            if (mouseLeftClicked or mouseRightClicked) and ClickBoard(mousex,mousey):   #如果点击了任一格子
                if mouseLeftClicked:                                #左键
                    if FirstClick==False:                           #检查是否为第一次点击，只有在第一次点击后，面板上才真正有雷
                        FirstClick=True
                        Blocks=RandomBOOM(Blocks,blockx,blocky)     #随机雷
                        Blocks=CalNumber(Blocks)                    #计算数字
                        RevealALL(Blocks)
                        startTime=time()
                        startTimeFlag=True
                    _,sign=CheckBlockStatus(Blocks,blocky,blockx)   #检查是否为旗子或问号，如果是，拒绝揭开格子
                    if sign==NONE:
                        BlockReveal(Blocks,blocky,blockx)
                elif mouseRightClicked:                             #右键
                    visit,sign=CheckBlockStatus(Blocks,blocky,blockx)
                    if visit==False:                                #空的标志->旗子->问号->空
                        if sign==NONE:
                            Blocks=ChangeBlockSign(Blocks,blocky,blockx,sign=FLAG)
                            boomnumber-=1
                        elif sign==FLAG:
                            Blocks=ChangeBlockSign(Blocks,blocky,blockx,sign=MISTERY)
                        elif sign==MISTERY:
                            Blocks=ChangeBlockSign(Blocks,blocky,blockx,sign=NONE)
                            boomnumber+=1

            mouseLeftClicked=False                                  #还原状态，以免忘记而出错,这里不加会出现右键1次出现问号的错误，很奇怪
            mouseRightClicked=False                                 #相应问题，包括“摁得太快”“滑动多选”
                                                                    #可能是get了两个事件，还在for里，没有还原导致
        if startTimeFlag:
            nowTime=time()
            alreadytime=int(nowTime-startTime)
            if alreadytime>=999:
                alreadytime=999
        if(boomnumber<0):
            boomnumber_screen=0
        else:
            boomnumber_screen=boomnumber
        pygame.display.update()
        FPSCLOCK.tick(ScreenFPS)

def ChangeBlockSign(Blocks,blocky,blockx,sign):         #更改为空，旗子，问号，三者之一
    Blocks[blocky][blockx].ChangeSign(sign)
    return Blocks

def CheckBlockStatus(Blocks,blocky,blockx):             #检查是否访问以及状态
    return Blocks[blocky][blockx].GetVisit(),Blocks[blocky][blockx].GetSign()

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
    i=blockx
    j=blocky
    if (i==0 and j==0) or (i==0 and j==ColNumber-1) or (i==RowNumber-1 and j==0) or (i==RowNumber-1 and j==ColNumber-1):
        safezone=4
    elif i==0 or i==RowNumber-1 or j==0 or j==ColNumber-1:
        safezone=6
    else:
        safezone=9

    for i in range(ColNumber*RowNumber-safezone):  #有一处和它的周边一定不为雷，在此设置安全区大小
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
            elif x-1<=blockx<=x+1 and y-1<=blocky<=y+1:
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

def DrawScreen(Blocks,Time,boomnumber):     #UI
    DrawButtonLine()
    for Blockrow in Blocks:
        for anyBlock in Blockrow:
            anyBlock.Draw()
    Time=str(Time)
    if len(Time)==1:
        Time="00"+Time
    elif len(Time)==2:
        Time="0"+Time
    DrawWord(Time,RED,TimePosx,TimePosy,TimeWidth,TimeHeight)
    boomnumber=str(boomnumber)
    if len(boomnumber)==1:
        boomnumber="0"+boomnumber
    elif len(boomnumber)==2:
        pass
    else:
        boomnumber="99"
    DrawWord(boomnumber,RED,BoomNumberPosx,BoomNumberPosy,BoomNumberWidth,BoomNumberHeight)

def DrawButtonLine():
    pygame.draw.rect(DISPLAYSURF,LIGHTGREY,(0,0,ScreenWidth,ButtonHeight))
    #pygame.draw.line(DISPLAYSURF,BLACK,(0,OthersHeight-1),(ScreenWidth//2,OthersHeight),1) #位置测试

def DrawWord(word,color,x,y,width,high,font=""):
    my_font=pygame.font.SysFont(font,1920)
    text=my_font.render(word,True,color)
    textPos=text.get_rect()
    text=pygame.transform.scale(text, (width,high))
    textPos.topleft=(x,y)
    DISPLAYSURF.blit(text,textPos)
    return text,textPos

class Rect():
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
            if self.GetSign()==NONE:    #没有标记
                pass
            elif self.GetSign()==FLAG:  #是旗子
                pygame.draw.polygon(DISPLAYSURF,DARKRED,((self.Getx()+RectWidthMiddle,self.Gety()+RectNumbery),(self.Getx()+RectWidthMiddle//3,self.Gety()+(RectHeightMiddle+RectNumbery)//2),(self.Getx()+RectWidthMiddle,self.Gety()+RectHeightMiddle)))
                pygame.draw.line(DISPLAYSURF,SILVERCOLOR,(self.Getx()+RectWidthMiddle,self.Gety()+RectNumbery),(self.Getx()+RectWidthMiddle,self.Gety()+RectHeight-RectNumbery),3)
            elif self.GetSign()==MISTERY:   #是问号
                DrawWord('?',BLACK,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)

        elif self.GetVisit()==True: #揭开了
            #如果是0123456789雷
            if self.GetContent()==BOOM:
                pygame.draw.rect(DISPLAYSURF,RED,(self.Getx()+RectEdge,self.Gety()+RectEdge,RectWidth-RectEdge*2,RectHeight-RectEdge*2),0)
            elif self.GetContent()==0:
                pass
            elif self.GetContent()==1:
                DrawWord('1',ONECOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)
            elif self.GetContent()==2:  #_|_|_
                DrawWord('2',TWOCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)
            elif self.GetContent()==3:  #_|_|_
                DrawWord('3',THREECOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)
            elif self.GetContent()==4:  #||_ 
                DrawWord('4',FOURCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)
            elif self.GetContent()==5:  #_|_|_
                DrawWord('5',FIVECOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)
            elif self.GetContent()==6:  #_|_||_
                DrawWord('6',SIXCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)
            elif self.GetContent()==7: #_||
                DrawWord('7',SEVENCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)
            elif self.GetContent()==8: #_||_||_
                DrawWord('8',EIGHTCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight)

if __name__=="__main__":
    main()
