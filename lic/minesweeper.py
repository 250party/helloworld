import pygame,sys
from pygame.locals import *
import random
from time import *
from math import pi as PI
from record import SaveRecord,LoadRecord
FLAG="flag"
MISTERY="mistery"
NONE="none"

SMILE="smile"
SAD="sad"
NORMAL="normal"

BOOM=-1

ScreenFPS=30            #刷新率
RowNumber=9             #RowRectNumber 一行有几个格子
ColNumber=9     
BOOMNumber=10           #雷的数目 
assert RowNumber>4
assert ColNumber>4
assert ColNumber*RowNumber>BOOMNumber
#对格子以及格子内容物的外观定义
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
#界面设计
ButtonHeight=20         #预留按钮高度
EdgeHeight=EdgeWidth=6  #面板间边界美化
FuncHeight=48           #计时，剩余雷数，重来方形区域高度
OthersHeight=ButtonHeight+EdgeHeight+FuncHeight+EdgeHeight  #其他高度总和
ScreenHeight=OthersHeight+RectHeight*ColNumber+EdgeHeight   #屏幕高度
ScreenWidth=EdgeWidth+RectWidth*RowNumber+EdgeWidth
#笑脸
SmileHeight=SmileWidth=FuncHeight*2//3      
SmilePosx=ScreenWidth//2-SmileWidth//2
SmilePosy=ButtonHeight+FuncHeight//3
#时间，剩余雷
TimePosx=ScreenWidth*2//3           
BoomNumberPosy=TimePosy=ButtonHeight+FuncHeight//3
BoomNumberHeight=TimeHeight=FuncHeight*2//3
TimeWidth=FuncHeight
BoomNumberPosx=ScreenWidth//4
BoomNumberWidth=FuncHeight*2//3
assert TimeWidth<ScreenWidth//3
assert BoomNumberWidth<ScreenWidth//2-BoomNumberPosx
#设置面板图形
SettingButtonPosx=2     #按钮               
SettingButtonPosy=1
SettingButtonHeight=ButtonHeight-2
SettingButtonWidth=40
Settingposx=EdgeWidth   #界面
Settingposy=ButtonHeight+EdgeHeight
SettingHeight=ScreenHeight-ButtonHeight-2*EdgeHeight
SettingWidth=ScreenWidth-2*EdgeWidth
SettingEdge=1
#颜色
WHITE=(255,255,255)
RED=(255,0,0)
LIGHTRED=(255,153,153)
DARKRED=(176,7,14)
SILVERCOLOR=(192,192,192)
LIGHTGREY=(224,224,224)
BLACK=(0,0,0)
LIGHTBLUE=(137,207,240)
YELLOW=(255,255,0)
ONECOLOR=(65,79,188)
TWOCOLOR=(33,98,1)
THREECOLOR=(168,3,6)
FOURCOLOR=(4,0,124)
FIVECOLOR=(123,1,0)
SIXCOLOR=(28,131,140)
SEVENCOLOR=(159,5,7)
EIGHTCOLOR=(169,9,11)

def main():
    global DISPLAYSURF,MY_FONT,SETTING_FONT,FPSCLOCK
    global EndBlockx,EndBlocky                      #结束时最后一个选择
    global RowNumber,ColNumber,BOOMNumber           #选择难度时更改这些值
    global ScreenHeight,ScreenWidth
    global SmilePosx,TimePosx,BoomNumberPosx,SettingWidth,SettingHeight

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((ScreenWidth,ScreenHeight))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('minesweeper')

    MY_FONT=pygame.font.SysFont("freesansbold",1920)    #字体设置
    SETTING_FONT=pygame.font.SysFont("arial",1920)

    Blocks=InitBoard()              #初始化空的内容

    mousex=0
    mousey=0
    FirstClick=False                #第1次点击标志，用于给内容赋值：雷1234567890
    startTimeFlag=False             #开始计时标志
    boomnumber_screen=boomnumber=BOOMNumber #显示的雷的数量。1.2.显示的数量，若不一致，刷新屏幕；3.全局变量

    pretime=0   #先前时间
    delTime=0   #时间差
    recordTime=999      #初始化变量，意思是从开始到结束所用时间

    preblockx=blockx=-1     #格子在数组的位置，pre意味着之前previous
    preblocky=blocky=-1

    smile_status=NORMAL     #板着脸

    DrawScreen(Blocks,blocky,blockx)    #绘制Setting横条，各个格子
    DrawTime(delTime)                   #绘制计时
    DrawBoomNumber(boomnumber_screen)   #绘制剩余雷数字
    DrawSmile(smile_status)             #绘制脸
    pygame.display.update()  #更新画面

    NeedChange=False        #主页面需要更新吗
    previsit=False          #先前访问的是哪一个，用于悬停边框绘制
    EndGameFlag=False       #结束游戏标志
    EndBlockx=-1
    EndBlocky=-1
    RevealAllFlag=False     #结束游戏时全部展示标志
    remainnumber=ColNumber*RowNumber-BOOMNumber    #剩余数量，用于胜利
    WinFlag=False           #保存记录用
    mouseLeftClicked=False
    mouseRightClicked=False
    
    SettingFlag=False       #开启设置功能的标志
    SettingScreenNeedChange=True    #设置面板更新的标志
    RestartFlag=False               #是否重来

    while True:
        if WinFlag:         #如果胜利，保存记录
            SaveRecord(RowNumber,ColNumber,BOOMNumber,recordTime)
            WinFlag=False
        while SettingFlag==True or (mouseLeftClicked and ClickedisSetting(mousex,mousey)):  #设置界面
            mouseLeftClicked=False
            for event in pygame.event.get():    #操作检测
                    if event.type==QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:     
                        if event.button==1:
                            mouseLeftClicked=True
                        mousex, mousey = event.pos
            if mouseLeftClicked and ClickedisSetting(mousex,mousey):    #退出设置
                SettingFlag=False
                NeedChange=True
                SettingScreenNeedChange=True
                mouseLeftClicked=False
                break
            
            SettingFlag=True        #持续while
            if SettingScreenNeedChange:         #更新画面，包括难度选择和记录展示
                TimeRecord=LoadRecord()
                DrawSettingScreen(TimeRecord)
                pygame.display.update()
                SettingScreenNeedChange=False   #别总是刷新
            
            if mouseLeftClicked:                #难度选择
                if ClickedisBeginner(mousex,mousey):
                    RowNumber=9       
                    ColNumber=9
                    BOOMNumber=10
                    RestartFlag=True
                elif ClickedisMediate(mousex,mousey):
                    RowNumber=16      
                    ColNumber=16
                    BOOMNumber=40
                    RestartFlag=True
                elif ClickedisAdvanced(mousex,mousey):
                    RowNumber=30       
                    ColNumber=16
                    BOOMNumber=99
                    RestartFlag=True
                if RestartFlag==True:       #要变更画面的高度和宽度，下面的也得跟着改；而且直接进到下面if里
                    ScreenHeight=OthersHeight+RectHeight*ColNumber+EdgeHeight   #屏幕高度
                    ScreenWidth=EdgeWidth+RectWidth*RowNumber+EdgeWidth
                    SmilePosx=ScreenWidth//2-SmileWidth//2
                    TimePosx=ScreenWidth*2//3           
                    BoomNumberPosx=ScreenWidth//4
                    SettingWidth=ScreenWidth-2*EdgeWidth
                    SettingHeight=ScreenHeight-ButtonHeight-2*EdgeHeight

                    DISPLAYSURF = pygame.display.set_mode((ScreenWidth,ScreenHeight))   #重设分辨率
                    SettingFlag=False
                    SettingScreenNeedChange=True
                    mouseLeftClicked=True
                    break
            FPSCLOCK.tick(ScreenFPS)
        
        if mouseLeftClicked and SettingFlag==False and (RestartFlag==True or ClickedisRestart(mousex,mousey)==True):  #重来，main照抄
            Blocks=InitBoard()

            mousex=0
            mousey=0
            FirstClick=False
            startTimeFlag=False
            boomnumber_screen=boomnumber=BOOMNumber #显示的雷的数量

            pretime=0   #先前时间
            delTime=0   #时间差

            preblockx=blockx=-1
            preblocky=blocky=-1

            smile_status=NORMAL

            DISPLAYSURF.fill(WHITE)
            DrawScreen(Blocks,blocky,blockx)
            DrawTime(delTime)
            DrawBoomNumber(boomnumber_screen)
            DrawSmile(smile_status)
            pygame.display.update()

            NeedChange=False        #需要更新屏幕吗
            previsit=False
            EndGameFlag=False       #结束游戏标志
            EndBlockx=-1
            EndBlocky=-1
            RevealAllFlag=False     #结束游戏是全部展示标志
            remainnumber=ColNumber*RowNumber-BOOMNumber    #剩余数量
            WinFlag=False
            mouseLeftClicked=False
            mouseRightClicked=False
            SettingFlag=False
            SettingScreenNeedChange=True
            RestartFlag=False

        if EndGameFlag:                       #游戏结束了
            if RevealAllFlag:
                RevealALL(Blocks)
                RevealAllFlag=False
        if NeedChange or pretime!=delTime:                     #仅在需要的时候刷新主界面
            DISPLAYSURF.fill(WHITE)
            DrawScreen(Blocks,preblocky,preblockx)
            DrawTime(delTime)
            DrawBoomNumber(boomnumber_screen)
            DrawSmile(smile_status)
            NeedChange=False
            pygame.display.update()         #刷新界面
        else:
            pass
        pretime=delTime
        mouseLeftClicked=False
        mouseRightClicked=False

        for event in pygame.event.get():    #操作检测
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:     #UP会有点不顺手
                if event.button==1:
                    mouseLeftClicked=True
                elif event.button==3:
                    mouseRightClicked=True
                mousex, mousey = event.pos

        if EndGameFlag==False and SettingFlag==False:              #游戏还没结束
            blockx,blocky= whatBlock(mousex,mousey)         #将鼠标位置转为雷的位置
            if blockx!=None and blocky!=None:               #如果鼠标放在了格子上
                visit,sign=CheckBlockStatus(Blocks,blocky,blockx)
                if visit==False:                            #画边框的，如果未曾访问过，就要追踪
                    if preblockx!=blockx or preblocky!=blocky:
                        NeedChange=True
                        preblockx=blockx
                        preblocky=blocky
                elif visit==True:                           #如果访问过了，那就不画，同时还要看是否是从有到无的时刻，以便刷新屏幕
                    preblockx=-1
                    preblocky=-1
                    if previsit!=visit:
                        NeedChange=True
                        previsit=visit
                if (mouseLeftClicked or mouseRightClicked):   #如果点击了任一格子
                    if mouseLeftClicked:                                #左键
                        if FirstClick==False:                           #检查是否为第一次点击，只有在第一次点击后，面板上才真正有雷
                            FirstClick=True
                            Blocks=RandomBOOM(Blocks,blockx,blocky)     #随机雷
                            Blocks=CalNumber(Blocks)                    #计算数字
                            startTimeFlag=True                          #开始计时

                        _,remainnumber=BlockReveal(Blocks,blocky,blockx,remainnumber)               #包含检查，连续揭开
                        if remainnumber==0:                             #如果剩下的都是雷
                            EndGameFlag=True
                            WinFlag=True
                            RevealAllFlag=True
                            smile_status=SMILE
                        if BlockisBOOM(Blocks,blocky,blockx):           #如果点到雷
                            EndGameFlag=True
                            RevealAllFlag=True
                            smile_status=SAD
                            EndBlockx=blockx*RectWidth+EdgeWidth
                            EndBlocky=blocky*RectHeight+OthersHeight
                        mouseLeftClicked=False

                    elif mouseRightClicked:                             #右键
                        if visit==False:                                #空的标志->旗子->问号->空
                            if sign==NONE:
                                Blocks=ChangeBlockSign(Blocks,blocky,blockx,sign=FLAG)
                                boomnumber-=1
                            elif sign==FLAG:
                                Blocks=ChangeBlockSign(Blocks,blocky,blockx,sign=MISTERY)
                            elif sign==MISTERY:
                                Blocks=ChangeBlockSign(Blocks,blocky,blockx,sign=NONE)
                                boomnumber+=1
                        mouseRightClicked=False
                    NeedChange=True
            #mouseLeftClicked=False                                  #还原状态，以免忘记而出错,这里不加会出现右键1次出现问号的错误，很奇怪
            #mouseRightClicked=False                                 #相应问题，包括“摁得太快”“滑动多选”,可能是get了两个事件，还在for里，没有还原导致。移出了for循环，但保留此处
            else:
                if preblockx!=-1 or preblocky!=-1:
                    preblockx=-1
                    preblocky=-1
                    NeedChange=True

            if FirstClick:
                if startTimeFlag:
                    startTime=time()                                    #开始计时
                    startTimeFlag=False
                currentTime=time()
                delTime=currentTime-startTime
                recordTime=delTime
                delTime=int(delTime)
                if delTime>=999:
                    delTime=999
            if boomnumber<0:
                boomnumber_screen=0
            else:
                boomnumber_screen=boomnumber

        #pygame.display.update()
        FPSCLOCK.tick(ScreenFPS)

def ClickedisSetting(mousex,mousey):
    Crect=pygame.Rect(SettingButtonPosx,SettingButtonPosy,SettingButtonWidth,SettingButtonHeight)
    if Crect.collidepoint(mousex,mousey):
        return True
    else:
        return False
    
def ClickedisRestart(mousex,mousey):
    Crect=pygame.Rect(SmilePosx,SmilePosy,SmileWidth,SmileHeight)
    if Crect.collidepoint(mousex,mousey):
        return True
    else:
        return False
    
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

def BlockReveal(Blocks,blocky,blockx,remainnumber):      #雷揭开
    if blocky<0 or blocky>ColNumber-1 or blockx<0 or blockx>RowNumber-1:    #递归越界中止
        return False,remainnumber
    visit,sign=CheckBlockStatus(Blocks,blocky,blockx)
    if sign==NONE and visit==False:                                         #递归中止2
        Blocks[blocky][blockx].ChangeVisit(True)
        if BlockisBOOM(Blocks,blocky,blockx)==False:
            remainnumber-=1
        if Blocks[blocky][blockx].GetContent()==0:                          #深度优先遍历
            _,remainnumber=BlockReveal(Blocks,blocky-1,blockx-1,remainnumber)
            _,remainnumber=BlockReveal(Blocks,blocky-1,blockx,remainnumber)
            _,remainnumber=BlockReveal(Blocks,blocky-1,blockx+1,remainnumber)
            _,remainnumber=BlockReveal(Blocks,blocky,blockx-1,remainnumber)
            _,remainnumber=BlockReveal(Blocks,blocky,blockx+1,remainnumber)
            _,remainnumber=BlockReveal(Blocks,blocky+1,blockx-1,remainnumber)
            _,remainnumber=BlockReveal(Blocks,blocky+1,blockx,remainnumber)
            _,remainnumber=BlockReveal(Blocks,blocky+1,blockx+1,remainnumber)
        return True,remainnumber
    return False,remainnumber
    
    
def whatBlock(mousex,mousey):   #将鼠标位置转为雷的位置
    if mousey<OthersHeight or mousey>=OthersHeight+ColNumber*RectHeight:  #不要随意等于，不然就把None检测考虑进去   
        return (None,None)
    elif mousex<EdgeWidth or mousex>=EdgeWidth+RowNumber*RectWidth:
        return (None,None)
    else:
        blockx=(mousex-EdgeWidth)//RectWidth
        blocky=(mousey-OthersHeight)//RectHeight
        return(blockx,blocky)
    
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

def DrawSmile(status):                      #绘制重来按钮
    pygame.draw.rect(DISPLAYSURF,BLACK,(SmilePosx,SmilePosy,SmileWidth,SmileHeight),1)
    pygame.draw.ellipse(DISPLAYSURF,YELLOW,(SmilePosx+1,SmilePosy+1,SmileWidth-2,SmileHeight-2),0)
    pygame.draw.circle(DISPLAYSURF,BLACK,(SmilePosx+SmileWidth//4,SmilePosy+SmileHeight//3),SmileWidth//12,0)
    pygame.draw.circle(DISPLAYSURF,BLACK,(SmilePosx+SmileWidth*3//4,SmilePosy+SmileHeight//3),SmileWidth//12,0)
    if status==NORMAL:
        pygame.draw.line(DISPLAYSURF,BLACK,(SmilePosx+SmileWidth//4,SmilePosy+SmileHeight*2//3),(SmilePosx+SmileWidth*3//4,SmilePosy+SmileHeight*2//3),1)
    elif status==SAD:
        pygame.draw.arc(DISPLAYSURF,BLACK,(SmilePosx+1+SmileWidth//4,SmilePosy+SmileHeight*2//3,(SmileWidth)//2,(SmileHeight)//3),0,PI,1)
    elif status==SMILE:
        pygame.draw.arc(DISPLAYSURF,BLACK,(SmilePosx+1+SmileWidth//4,SmilePosy+SmileHeight//2,(SmileWidth)//2,(SmileHeight)//3),PI,PI*2,1)

def DrawTime(Time):
    Time=str(Time)                          #画时间
    if len(Time)==1:
        Time="00"+Time
    elif len(Time)==2:
        Time="0"+Time
    DrawWord(Time,RED,TimePosx,TimePosy,TimeWidth,TimeHeight,MY_FONT)

def DrawBoomNumber(boomnumber):
    boomnumber=str(boomnumber)              #画雷的数量
    if len(boomnumber)==1:
        boomnumber="0"+boomnumber
    elif len(boomnumber)==2:
        pass
    else:
        boomnumber="99"
    DrawWord(boomnumber,RED,BoomNumberPosx,BoomNumberPosy,BoomNumberWidth,BoomNumberHeight,MY_FONT)

def DrawScreen(Blocks,blocky,blockx):     #UI
    DrawButtonLine()                        #画按钮横条
    i=0
    for Blockrow in Blocks:                 #画格子
        j=0
        for anyBlock in Blockrow:
            anyBlock.Draw()
            if blocky==i and blockx==j:     #在鼠标悬停处绘制边框
                anyBlock.DrawLight(i,j)
            j+=1
        i+=1

def DrawButtonLine():
    pygame.draw.rect(DISPLAYSURF,LIGHTGREY,(0,0,ScreenWidth,ButtonHeight))
    DrawWord("Setting",BLACK,SettingButtonPosx,SettingButtonPosy,SettingButtonWidth,SettingButtonHeight,SETTING_FONT)
    #pygame.draw.line(DISPLAYSURF,BLACK,(0,OthersHeight-1),(ScreenWidth//2,OthersHeight),1) #位置测试

def DrawWord(word,color,x,y,width,high,FONT):
    FONT=FONT
    text=FONT.render(word,True,color)
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
                DrawWord('?',BLACK,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)

        elif self.GetVisit()==True: #揭开了
            #如果是0123456789雷
            if self.GetContent()==BOOM:             #淡红色，作为没揭开的点
                pygame.draw.rect(DISPLAYSURF,LIGHTRED,(self.Getx()+RectEdge,self.Gety()+RectEdge,RectWidth-RectEdge*2,RectHeight-RectEdge*2),0)
            elif self.GetContent()==0:
                pass
            elif self.GetContent()==1:
                DrawWord('1',ONECOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
            elif self.GetContent()==2:  #_|_|_
                DrawWord('2',TWOCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
            elif self.GetContent()==3:  #_|_|_
                DrawWord('3',THREECOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
            elif self.GetContent()==4:  #||_ 
                DrawWord('4',FOURCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
            elif self.GetContent()==5:  #_|_|_
                DrawWord('5',FIVECOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
            elif self.GetContent()==6:  #_|_||_
                DrawWord('6',SIXCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
            elif self.GetContent()==7: #_||
                DrawWord('7',SEVENCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
            elif self.GetContent()==8: #_||_||_
                DrawWord('8',EIGHTCOLOR,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)

            if self.Getx()==EndBlockx and self.Gety()==EndBlocky:     #预留作为结束点，红色醒目
                pygame.draw.rect(DISPLAYSURF,RED,(self.Getx()+RectEdge,self.Gety()+RectEdge,RectWidth-RectEdge*2,RectHeight-RectEdge*2),0)
            if self.GetSign()==FLAG:                    #在最后全部揭开时作为错误的插旗使用
                pygame.draw.polygon(DISPLAYSURF,DARKRED,((self.Getx()+RectWidthMiddle,self.Gety()+RectNumbery),(self.Getx()+RectWidthMiddle//3,self.Gety()+(RectHeightMiddle+RectNumbery)//2),(self.Getx()+RectWidthMiddle,self.Gety()+RectHeightMiddle)))
                pygame.draw.line(DISPLAYSURF,SILVERCOLOR,(self.Getx()+RectWidthMiddle,self.Gety()+RectNumbery),(self.Getx()+RectWidthMiddle,self.Gety()+RectHeight-RectNumbery),3)
            elif self.GetSign()==MISTERY:               #是问号
                DrawWord('?',BLACK,self.Getx()+RectNumberx,self.Gety()+RectNumbery,RectNumberWidth,RectNumberHeight,MY_FONT)
    def DrawLight(self,by,bx):
        pygame.draw.rect(DISPLAYSURF,LIGHTBLUE,(bx*RectWidth+EdgeWidth,by*RectHeight+OthersHeight,RectWidth,RectHeight),RectEdge+1)

def DrawSettingScreen(record):
    pygame.draw.rect(DISPLAYSURF,BLACK,(Settingposx,Settingposy,SettingWidth,SettingHeight),SettingEdge)
    pygame.draw.rect(DISPLAYSURF,WHITE,(Settingposx+SettingEdge,Settingposy+SettingEdge,SettingWidth-SettingEdge*2,SettingHeight-SettingEdge*2),0)
    DrawWord("Your Record:",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingEdge*2,SettingButtonWidth*2,SettingButtonHeight,SETTING_FONT)
    DrawWord("1."+"beginner",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight+SettingEdge*2,SettingButtonWidth*1.8,SettingButtonHeight,SETTING_FONT)
    DrawWord("  "+"time:"+str(record["timescore"][0]["最好用时"]),BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*2+SettingEdge*2,SettingButtonWidth+len(str(record["timescore"][0]["最好用时"]))*8,SettingButtonHeight,SETTING_FONT)        
    DrawWord("2."+"mediate ",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*3+SettingEdge*2,SettingButtonWidth*1.8,SettingButtonHeight,SETTING_FONT)
    DrawWord("  "+"time:"+str(record["timescore"][1]["最好用时"]),BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*4+SettingEdge*2,SettingButtonWidth+len(str(record["timescore"][1]["最好用时"]))*8,SettingButtonHeight,SETTING_FONT) 
    DrawWord("3."+"advanced",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*5+SettingEdge*2,SettingButtonWidth*1.8,SettingButtonHeight,SETTING_FONT)
    DrawWord("  "+"time:"+str(record["timescore"][2]["最好用时"]),BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*6+SettingEdge*2,SettingButtonWidth+len(str(record["timescore"][2]["最好用时"]))*8,SettingButtonHeight,SETTING_FONT) 

    DrawWord("Choose Difficulty:",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*8+SettingEdge,SettingButtonWidth*3,SettingButtonHeight,SETTING_FONT)
    pygame.draw.rect(DISPLAYSURF,BLACK,(Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*9.5+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight),1)
    DrawWord("Beginner ",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*9.5+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight,SETTING_FONT)
    pygame.draw.rect(DISPLAYSURF,BLACK,(Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*11+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight),1)
    DrawWord("Mediate  ",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*11+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight,SETTING_FONT)
    pygame.draw.rect(DISPLAYSURF,BLACK,(Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*12.5+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight),1)
    DrawWord("Advanced",BLACK,Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*12.5+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight,SETTING_FONT)

def ClickedisBeginner(mousex,mousey):
    Crect=pygame.Rect(Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*9.5+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight)
    if Crect.collidepoint(mousex,mousey):
        return True
    else:
        return False
    
def ClickedisMediate(mousex,mousey):
    Crect=pygame.Rect(Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*11+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight)
    if Crect.collidepoint(mousex,mousey):
        return True
    else:
        return False
    
def ClickedisAdvanced(mousex,mousey):
    Crect=pygame.Rect(Settingposx+SettingEdge*2,Settingposy+SettingButtonHeight*12.5+SettingEdge,SettingButtonWidth*1.8,SettingButtonHeight)
    if Crect.collidepoint(mousex,mousey):
        return True
    else:
        return False
if __name__=="__main__":
    main()
