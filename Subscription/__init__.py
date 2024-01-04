# coding=utf-8
from .compareData import *
from hoshino import Service
from hoshino.typing import HoshinoBot,CQEvent
from nonebot import get_bot

sv = Service("雀魂对局订阅")


@sv.on_prefix("雀魂订阅")
async def orderInfo(bot, ev: CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    IDdata = await getID(nickname,4)
    message = ""
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次再进行订阅")
    else:
        if len(IDdata) > 1:
            gid = ev["group_id"]
            playerRecord = await selectRecord(IDdata[0]["id"],4)  # 获取对局记录
            if jsonWriter(playerRecord, gid, IDdata[0]["id"],4):
                message = message + "查询到多条角色昵称呢~，若订阅不是您想订阅的昵称，请补全昵称后重试\n"
                message = message + "昵称:" + str(IDdata[0]["nickname"]) + " 的对局已订阅成功"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)
        else:
            gid = ev["group_id"]
            playerRecord = await selectRecord(IDdata[0]["id"],4) #获取对局记录
            if jsonWriter(playerRecord,gid,IDdata[0]["id"],4):
                message = message + "昵称:" + str(IDdata[0]["nickname"])+" 的对局已订阅成功"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)

@sv.on_prefix(("关闭雀魂订阅","取消雀魂订阅"))
async def cancelOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    gid = ev["group_id"]
    message = ""
    record = localLoad(4)
    flag = False
    IDdata = await getID(nickname,4)
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    datalist=[]
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = False
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +" 在本群的四麻订阅已成功关闭")
        else:
            await bot.finish(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试")

@sv.on_prefix("开启雀魂订阅")
async def openOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    gid = ev["group_id"]
    record = localLoad(4)
    flag = False
    IDdata = await getID(nickname,4)
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    message = ""
    datalist=[]
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = True
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +"在本群的四麻订阅已成功开启")
        else:
            await bot.send(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试")

@sv.scheduled_job('interval', minutes=3)
async def record_scheduled():
    bot = get_bot()
    record = localLoad(4)
    for i in range(0,len(record)):
        playerRecord = await selectRecord(record[i]["id"],4)
        if playerRecord == -1:
            sv.logger.info("获取" + str(record[i]["id"]) + "的对局数据超时已自动跳过")
            continue
        compareRecord = json.loads(playerRecord)
        sv.logger.info("正在检测更新"+str(record[i]["id"])+"的对局数据")
        if int(record[i]["endTime"]) < int(compareRecord[0]["endTime"]):
            message = updateData(playerRecord,record[i]["gid"],record[i]["id"],4)
            await bot.send_group_msg(group_id=int(record[i]["gid"]),message=message)

@sv.on_fullmatch("雀魂订阅状态")
async def orderSituation(bot,ev):
    gid = ev["group_id"]
    datalist = []
    message = ""
    record = localLoad(4)
    for i in range(0,len(record)):
        if int(record[i]["gid"]) == int(gid):
            datalist.append(record[i])
    if len(datalist) == 0:
        print(len(datalist))
        await bot.finish(ev,"本群还没有雀魂对局的订阅哦~")
    else:
        message = message + "已查询到群"+str(gid)+"的订阅状态:\n"
        for i in range(0,len(datalist)):
            data = await selectNickname(datalist[i]["id"],"4")
            sv.logger.info("正在获取"+str(datalist[i]["id"])+"的昵称信息")
            if data == -1:
                await bot.finish(ev, "获取昵称信息失败，请重试")
            else:
                message = message + "昵称：" + data + "   "
            if datalist[i]["record_on"]:
                message = message + "开启\n"
            else:
                message = message + "关闭\n"
        await bot.send(ev,message)


@sv.on_prefix("删除雀魂订阅")
async def delInfo(bot,ev):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    gid = ev["group_id"]
    record = localLoad(4)
    flag = False
    IDdata = await getID(nickname,4)
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    datalist = []
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0, len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"] == record[i]["id"]:
                flag = True
                continue
            else:
                datalist.append(record[i])
        if flag:
            with open(join(path, 'account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev, "该昵称在本群的四麻订阅已删除")
        else:
            await bot.send(ev, "没有找到该昵称在本群的订阅记录哦，请检查后重试")

@sv.on_prefix("三麻订阅")
async def orderTriInfo(bot, ev: CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    IDdata = await getID(nickname,3)
    message = ""
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次再进行订阅")
    else:
        if len(IDdata) > 1:
            gid = ev["group_id"]
            playerRecord = await selectRecord(IDdata[0]["id"],3)  # 获取对局记录
            if jsonWriter(playerRecord, gid, IDdata[0]["id"],3):
                message = message + "查询到多条角色昵称呢~，若订阅不是您想订阅的昵称，请补全昵称后重试\n"
                message = message + "昵称:" + str(IDdata[0]["nickname"]) + " 的对局已订阅成功"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)
        else:
            gid = ev["group_id"]
            playerRecord = await selectRecord(IDdata[0]["id"],3) #获取对局记录
            if jsonWriter(playerRecord,gid,IDdata[0]["id"],3):
                message = message + "昵称:" + str(IDdata[0]["nickname"])+" 的对局已订阅成功"
            else:
                message = message + "该昵称在本群已被订阅，请不要重新订阅哦！"
            await bot.send(ev, message)

@sv.on_prefix(("关闭三麻订阅","取消三麻订阅"))
async def cancelTriOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    gid = ev["group_id"]
    message = ""
    record = localLoad(3)
    flag = False
    IDdata = await getID(nickname,3)
    datalist=[]
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = False
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'tri_account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +" 在本群的三麻订阅已成功关闭")
        else:
            await bot.send(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试")

@sv.on_prefix("开启三麻订阅")
async def openTriOrder(bot,ev:CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    gid = ev["group_id"]
    record = localLoad(3)
    flag = False
    IDdata = await getID(nickname,3)
    message = ""
    datalist=[]
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0,len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"]==record[i]["id"]:
                message = message + IDdata[0]["nickname"]
                record[i]["record_on"] = True
                flag = True
            datalist.append(record[i])
        if flag:
            with open(join(path, 'tri_account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev,"昵称:"+ message +"在本群的三麻订阅已成功开启")
        else:
            await bot.send(ev,"没有找到该昵称在本群的订阅记录哦，请检查后重试")

@sv.scheduled_job('interval', minutes=5)
async def Trirecord_scheduled():
    bot = get_bot()
    record = localLoad(3)
    for i in range(0,len(record)):
        playerRecord = await selectRecord(record[i]["id"],3)
        if playerRecord == -1:
            sv.logger.info("获取" + str(record[i]["id"]) + "的三麻对局数据超时已自动跳过")
            continue
        compareRecord = json.loads(playerRecord)
        sv.logger.info("正在检测更新"+str(record[i]["id"])+"的三麻对局数据")
        if int(record[i]["endTime"]) < int(compareRecord[0]["endTime"]):
            message = updateData(playerRecord,record[i]["gid"],record[i]["id"],3)
            await bot.send_group_msg(group_id=int(record[i]["gid"]),message=message)

@sv.on_fullmatch("三麻订阅状态")
async def orderSituation(bot,ev):
    gid = ev["group_id"]
    datalist = []
    message = ""
    record = localLoad(3)
    for i in range(0,len(record)):
        if int(record[i]["gid"]) == int(gid):
            datalist.append(record[i])
    if datalist == []:
        await bot.finish(ev,"本群还没有雀魂三麻对局的订阅哦~")
    else:
        message = message + "已查询到群"+str(gid)+"的订阅状态:\n"
        for i in range(0,len(datalist)):
            data = await selectNickname(datalist[i]["id"],"3")
            sv.logger.info("正在获取" + str(datalist[i]["id"]) + "的昵称信息")
            if data == -1:
                await bot.finish(ev, "获取昵称信息失败，请重试")
            else:
                message = message + "昵称：" + data + "    "
            if datalist[i]["record_on"]:
                message = message + "开启\n"
            else:
                message = message + "关闭\n"
        await bot.send(ev,message)

@sv.on_prefix("删除三麻订阅")
async def delTriInfo(bot,ev):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        await bot.finish(ev, "昵称长度超过雀魂最大限制")
    gid = ev["group_id"]
    record = localLoad(3)
    flag = False
    IDdata = await getID(nickname,3)
    datalist = []
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~\n请在金之间以上房间对局一次后重试")
    else:
        for i in range(0, len(record)):
            if int(record[i]["gid"]) == int(gid) and IDdata[0]["id"] == record[i]["id"]:
                flag = True
                continue
            else:
                datalist.append(record[i])
        if flag:
            with open(join(path, 'tri_account.json'), 'w', encoding='utf-8') as fp:
                json.dump(datalist, fp, indent=4)
            await bot.send(ev, "该昵称在本群的三麻订阅已删除")
        else:
            await bot.send(ev, "没有找到该昵称在本群的订阅记录哦，请检查后重试")