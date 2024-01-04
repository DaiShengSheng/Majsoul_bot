# coding=utf-8
import aiohttp
from os.path import dirname,join
import urllib.request
import urllib.error
import urllib.parse
import json
import time

baseurl = "https://ak-data-1.sapk.ch/api/v2/pl4"
tribaseurl = "https://ak-data-1.sapk.ch/api/v2/pl3"
path = dirname(__file__)


async def getURL(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        async with aiohttp.ClientSession() as session:
            async with await session.get(url=url,headers=headers) as response:
                info = await response.text()
    except:
        return "error"
    return info

async def getID(nickname,num):#获取牌谱屋角色ID
    nickname = urllib.parse.quote(nickname) #UrlEncode转换
    if num == 4:
        url = baseurl + "/search_player/"+nickname+"?limit=9"
    else:
        url = tribaseurl + "/search_player/" + nickname + "?limit=9"
    data = await getURL(url)
    if data == "error":
        return -404
    datalist = json.loads(data)
    if datalist == [] :
        return -1
    return datalist

async def selectRecord(id,num):
    localtime = time.time()
    urltime = str(int(localtime * 1000))  # 时间戳
    if num == 4:
        basicurl = baseurl + "/player_stats/" + str(id) + "/1262304000000/" + urltime + "?mode=16.12.9.15.11.8"
    else:
        basicurl = tribaseurl + "/player_stats/" + str(id) + "/1262304000000/" + urltime + "?mode=22.24.26.21.23.25"
    data = await getURL(basicurl)
    if data == "error":
        return -1
    count = str(json.loads(data)["count"])
    if num == 4:
        recordurl = baseurl + "/player_records/"+str(id)+"/"+urltime+"/1262304000000?limit=2&mode=16.12.9.15.11.8&descending=true&tag="+count
    else:
        recordurl = tribaseurl + "/player_records/"+str(id)+"/"+urltime+"/1262304000000?limit=2&mode=22.24.26.21.23.25&descending=true&tag="+count
    record = await getURL(recordurl)
    if record == "error":
        return -1
    return record

def localLoad(num):
    if num == 4:
        with open(join(path,'account.json'),encoding='utf-8') as fp:
            data = json.load(fp)
    #print(data[0]["uuid"])
    else:
        with open(join(path,'tri_account.json'),encoding='utf-8') as fp:
            data = json.load(fp)
    return data


def jsonWriter(Record,gid,id,num):
    localdata = localLoad(num)
    data = json.loads(Record)
    datalist = []
    for i in range(0,len(localdata)):
        if localdata[i]["gid"] == str(gid) and localdata[i]["id"] == id:
            return False
        datalist.append(localdata[i])
    binds = {
        "id": id,
        "uuid": str(data[0]["uuid"]),
        "endTime": int(data[0]["endTime"]),
        "gid": str(gid),
        "record_on": True,
    }
    datalist.append(binds)
    if num == 4:
        with open(join(path,'account.json'),'w',encoding='utf-8') as fp:
            json.dump(datalist,fp,indent=4)
    else:
        with open(join(path, 'tri_account.json'), 'w', encoding='utf-8') as fp:
            json.dump(datalist, fp, indent=4)
    return True
