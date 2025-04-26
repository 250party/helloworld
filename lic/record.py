import json

def SaveRecord(RowRectNumber,ColRectNumber,BoomNumber,deltime):
    if RowRectNumber==9 and ColRectNumber==9 and BoomNumber==10:
        key="初级"
    elif RowRectNumber==16 and ColRectNumber==16 and BoomNumber==40:
        key="中级"
    elif RowRectNumber==30 and ColRectNumber==16 and BoomNumber==99:
        key="高级"
    else: 
        return 0
    data=LoadRecord()
    recording=data["timescore"]
    for anyRecord in recording:
        if anyRecord["难度"]==key:
            if deltime<anyRecord["最好用时"]:
                anyRecord["最好用时"]=deltime

    with open("./minesweeperdata/time_record.json",'w',encoding='utf-8')as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def LoadRecord():
    try:
        with open('./minesweeperdata/time_record.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        with open('./minesweeperdata/time_record.json', 'w', encoding='utf-8') as f:
            data1={
                "难度":"初级",
                "最好用时":999
            }
            data2={
                "难度":"中级",
                "最好用时":999
            }
            data3={
                "难度":"高级",
                "最好用时":999
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