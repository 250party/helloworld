import json

def SaveRecord(RowRectNumber,ColRectNumber,BoomNumber,deltime,Win=False):
    if RowRectNumber==9 and ColRectNumber==9 and BoomNumber==10:
        key="初级"
    elif RowRectNumber==16 and ColRectNumber==16 and BoomNumber==40:
        key="中级"
    elif RowRectNumber==30 and ColRectNumber==16 and BoomNumber==99:
        key="高级"
    else: 
        return 0
    data=LoadRecord()
    #print(data)
    recording=data["timescore"]
    for anyRecord in recording:
        if anyRecord["难度"]==key:
            print(anyRecord["局数"],int(float(anyRecord["局数"])))
            anyRecord["局数"]=int(float(anyRecord["局数"]))+1
            print(anyRecord["局数"])
            if Win==True:
                if deltime<float(anyRecord["最好用时"]):
                    deltime=format(deltime,'.4f')
                    anyRecord["最好用时"]=deltime
                anyRecord["胜利局数"]=int(float(anyRecord["胜利局数"]))+1
                anyRecord["胜率"]=float(anyRecord["胜利局数"]/float(anyRecord["局数"])) if float(anyRecord["局数"])!=0 else 0

    with open("./minesweeperdata/time_record.json",'w',encoding='utf-8')as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def LoadRecord():
    try:
        with open('./minesweeperdata/time_record.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except MemoryError:
        raise MemoryError("内存溢出")
    except PermissionError:
        raise PermissionError("不允许访问文件")
    except Exception:        #只要出错就重新初始化
        data=InitRecord()
    return data
    
def InitRecord():
    with open('./minesweeperdata/time_record.json', 'w', encoding='utf-8') as f:
        data1={
            "难度":"初级",
            "最好用时":999,
            "局数":0,
            "胜利局数":0,
            "胜率":0
        }
        data2={
            "难度":"中级",
            "最好用时":999,
            "胜利局数":0,
            "局数":0,
            "胜率":0
        }
        data3={
            "难度":"高级",
            "最好用时":999,
            "胜利局数":0,
            "局数":0,
            "胜率":0
        }
        data={
            "timescore":[data1,data2,data3]
            }
        json.dump(data, f, indent=4)
    return data
def main():
    SaveRecord(9,9,10,100)
if __name__=='__main__':
    main()