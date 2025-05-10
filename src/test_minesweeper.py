from minesweeper import *
import minesweeper as MS
import pandas as pd
import pytest
#-q quiet

#测试碰撞
@pytest.mark.skip
@pytest.mark.parametrize("a, b, expected", [    #(2,1)设置按钮的左上角坐标,经测试右下角碰撞坐标为(50,18),而按钮的高度和宽度初始设为18,49,一共18,49个像素
    (2, 1, True),      #True   
    (2-1, 1, False),      #F
    (2, 1-1, False),      #F
    (2+1, 1, True),   #T
    (2+49, 1, False),    #False
    (2+49-1, 1, True),   #T
    (2+49+1, 1, False),   #F
    (2, 1+18, False),   #False
    (2, 1+18-1, True),   #T
    (2, 1+18+1, False),   #F
])
def test_click(a, b, expected):         #测试按钮碰撞
    assert ClickedisSetting(a,b) == expected

#测试碰撞
def printinitboard():    #如第1个格子(6,80),第二个格子(38,80),猜测第1个格子的背景从(7,81)到(36,81),第1个格子的背景从(39,81)到......
    Blocks=InitBoard()
    for i in Blocks:
        for j in i:
            print(j.Getx(),j.Gety(),end='\t\t')
        print()

@pytest.mark.skip
@pytest.mark.parametrize("a, b, expected", [    #第1个格子(6,80),第二个格子(38,80)，测试左上角格子的位置是否与预期一致
    (6, 80, (0,0)),       
    (6-1, 80, (None,None)),      
    (6, 80-1, (None,None)),      
    (6+1, 80, (0,0)),   
    (6+32, 80, (1,0)),    
    (6+32-1, 80, (0,0)),   
    (6+32+1, 80, (1,0)),   
    (6, 80+32, (0,1)),   
    (6, 80+32-1, (0,0)),   
    (6, 80+32+1, (0,1)),   
])
def test_clickRectLeft(a, b, expected):         #测试按钮碰撞
    assert whatBlock(a,b) == expected

@pytest.mark.skip
@pytest.mark.parametrize("a, b, expected", [    #测试右下角格子的位置是否与预期一致
    (262, 336, (8,8)),       
    (262-1, 336, (7,8)),      
    (262, 336-1, (8,7)),      
    (262+1, 336, (8,8)),   
    (262+32, 336, (None,None)),    
    (262+32-1, 336, (8,8)),   
    (262+32+1, 336, (None,None)),   
    (262, 336+32, (None,None)),   
    (262, 336+32-1, (8,8)),   
    (262, 336+32+1, (None,None)),   
])
def test_clickRectRight(a, b, expected):         #测试按钮碰撞
    assert whatBlock(a,b) == expected

@pytest.mark.skip                               #测试随机雷的数量
@pytest.mark.parametrize("x, y", [    
    (0,0),
    (0,1),
    (8,8),
    (5,5),
    #(None,None)     #这种情况在组合的时候不会出现
])
def test_randomboom(x,y):
    Blocks=InitBoard()
    assert sum(num.GetContent() for row in RandomBOOM(Blocks,x,y) for num in row)==-10

@pytest.mark.skip                              
@pytest.mark.parametrize("x, y", [    
    (0,0),
    (0,1),
    (8,8),
    (5,5),
])
def test_calnum(x,y):           #测试雷周围的数字,可以用图形化界面吗
    #MS.ColNumber=16
    #MS.RowNumber=30
    #MS.BOOMNumber=99
    Blocks=InitBoard()
    Blocks=RandomBOOM(Blocks,x,y)
    Blocks=CalNumber(Blocks)
    print()
    Contents=pd.DataFrame([[any.GetContent() for any in row]for row in Blocks])
    print(Contents)
    assert Blocks[y][x].GetContent()==0

@pytest.mark.skip                              
@pytest.mark.parametrize("x, y", [    
    (0,0),
    (0,1),
    (8,8),
    (5,5),
    (-1,-1),
    (9,8)
])       
def test_blockreveal(x,y):
    Blocks=InitBoard()
    try:
        Blocks=RandomBOOM(Blocks,x,y)
    except Exception:
        Blocks=RandomBOOM(Blocks,0,0)
    Blocks=CalNumber(Blocks)
    status,remainnumber=BlockReveal(Blocks,x,y,81)
    print()
    Contents=pd.DataFrame([[(any.GetContent(),any.GetVisit()) for any in row]for row in Blocks])
    print(Contents)
    assert remainnumber >= 0



if __name__=="__main__":
    pytest.main(['-q','-s'])
    #pytest.main(['--collect-only'])
    #printinitboard()
    pass