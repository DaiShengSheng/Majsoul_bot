from .RecordLoader import *

def updateData(record,gid):
    localdata = localLoad()
    data = json.loads(record)
    datalist = []
    message = ""
    for i in range(0,len(localdata)):
        if data[1]["uuid"] == localdata[i]["uuid"] and gid == localdata[i]["gid"]:
            localdata[i]["uuid"] = data[0]["uuid"]
            localdata[i]["endTime"] = data[0]["endTime"]
            if localdata[i]["record_on"]:
                message = message + processdata(data)
        datalist.append(localdata[i])
    with open(join(path,'account.json'),'w',encoding='utf-8') as fp:
        json.dump(datalist,fp,indent=4)
    return message

def processdata(data):
    message = "本群侦测到新的对局："
    message = message + "\n牌谱ID：" + str(data[0]["uuid"]) + "\n"
    for j in range(0, 4):
        message = message + str(data[0]["players"][j]["nickname"]) + "(" + str(data[0]["players"][j]["score"]) + ")  "
    message = message + "\n"
    message = message + "对局开始时间：" + str(convertTime(data[0]["startTime"])) + "  "
    message = message + "对局结束时间：" + str(convertTime(data[0]["endTime"])) + "  \n"
    return message

def convertTime(datatime):
    timeArray = time.localtime(datatime)
    Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return Time

def selectNickname(id):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳
    basicurl = baseurl + "/player_stats/" + str(id) + "/1262304000000/" + urltime + "?mode=16.12.9.15.11.8"
    nickname = str(json.loads(getURL(basicurl))["nickname"])
    return nickname
