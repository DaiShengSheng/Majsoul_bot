# coding=utf-8
from .processData import *
from hoshino import Service
from hoshino.typing import HoshinoBot,CQEvent

sv = Service("雀魂信息查询")

@sv.on_prefix(('雀魂信息','雀魂查询'))
async def majsoulInfo(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args) == 1:
        nickname = ev.message.extract_plain_text()
        if len(nickname) > 15:
            await bot.finish(ev, "昵称长度超过雀魂最大限制")
        message = "\n"
        IDdata = getID(nickname)
        if IDdata == -404:
            await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
        sv.logger.info("正在查询" + nickname + "的对局数据")
        if IDdata == -1:
            await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~")
        else:
            if len(IDdata)>1:
                message = message + "查询到多条角色昵称呢~，若输出不是您想查找的昵称，请补全查询昵称\n\n"
                message = message + printBasicInfo(IDdata[0],"0","4")
                await bot.send(ev, message, at_sender=True)
            else:
                message = message+printBasicInfo(IDdata[0],"0","4")
                await bot.send(ev,message,at_sender=True)
    elif len(args) == 2:
        nickname = args[1]
        if len(nickname) > 15:
            await bot.finish(ev, "昵称长度超过雀魂最大限制")
        sv.logger.info("正在查询" + nickname + "的对局数据 ")
        message = "\n"
        room_level = ""
        if args[0] == "金场" or args[0] == "金" or args[0] == "金之间":
            room_level = "1"
        elif args[0] == "玉场" or args[0] == "玉" or args[0] == "玉之间":
            room_level = "2"
        elif args[0] == "王座" or args[0] == "王座之间":
            room_level = "3"
        else:
            await bot.finish(ev, "房间等级输入不正确，请重新输入",at_sender=True)
        IDdata = getID(nickname)
        if IDdata == -404:
            await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
        if IDdata == -1:
            await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~")
        else:
            if len(IDdata) > 1:
                message = message + "查询到多条角色昵称呢~，若输出不是您想查找的昵称，请补全查询昵称\n"
                message = message + printExtendInfo(IDdata[0], room_level,"4")
                await bot.send(ev, message, at_sender=True)
            else:
                pic = printExtendInfo(IDdata[0], room_level,"4")
                await bot.send(ev, pic, at_sender=True)
    else:
        await bot.finish(ev, "查询信息输入不正确，请重新输入", at_sender=True)


@sv.on_prefix(('雀魂牌谱','牌谱查询'))
async def RecordInfo(bot, ev: CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        sv.logger.info("昵称长度超过雀魂最大限制，已跳过")
        return
    IDdata = getID(nickname)
    if IDdata == -404:
        await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
    message = "\n"
    sv.logger.info("正在查询" + nickname + "的牌谱数据")
    if IDdata == -1:
        await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~")
    else:
        if len(IDdata) > 1:
            message = message + "查询到多条角色昵称呢~，若输出不是您想查找的昵称，请补全查询昵称\n"
            message = message + printRecordInfo(IDdata[0],4)
            await bot.send(ev, message, at_sender=True)
        else:
            message = message + printRecordInfo(IDdata[0],4)
            await bot.send(ev, message, at_sender=True)

@sv.on_prefix(('三麻信息','三麻查询'))
async def TrimajsoulInfo(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args) == 1:
        nickname = ev.message.extract_plain_text()
        if len(nickname) > 15:
            await bot.finish(ev, "昵称长度超过雀魂最大限制")
        message = "\n"
        sv.logger.info("正在查询" + nickname + "的对局数据")
        IDdata = gettriID(nickname)
        if IDdata == -404:
            await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
        if IDdata == -1:
            await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~")
        else:
            if len(IDdata)>1:
                message = message + "查询到多条角色昵称呢~，若输出不是您想查找的昵称，请补全查询昵称\n\n"
                message = message + printBasicInfo(IDdata[0],"0","3")
                await bot.send(ev, message, at_sender=True)
            else:
                message = message + printBasicInfo(IDdata[0],"0","3")
                await bot.send(ev,message,at_sender=True)
    elif len(args) == 2:
        if len(nickname) > 15:
            await bot.finish(ev, "昵称长度超过雀魂最大限制")
        nickname = args[1]
        sv.logger.info("正在查询" + nickname + "的对局数据")
        message = "\n"
        room_level = ""
        if args[0] == "金场" or args[0] == "金" or args[0] == "金之间":
            room_level = "1"
        elif args[0] == "玉场" or args[0] == "玉" or args[0] == "玉之间":
            room_level = "2"
        elif args[0] == "王座" or args[0] == "王座之间":
            room_level = "3"
        else:
            await bot.finish(ev, "房间等级输入不正确，请重新输入",at_sender=True)
        sv.logger.info("正在查询" + nickname + "的对局数据")
        IDdata = gettriID(nickname)
        if IDdata == -404:
            await bot.finish(ev, "获取牌谱屋的数据超时了呢，请稍后再试哦~")
        if IDdata == -1:
            await bot.finish(ev, "没有查询到该角色在金之间以上的对局数据呢~")
        else:
            if len(IDdata) > 1:
                message = message + "查询到多条角色昵称呢~，若输出不是您想查找的昵称，请补全查询昵称\n"
                message = message + printExtendInfo(IDdata[0], room_level,"3")
                await bot.send(ev, message, at_sender=True)
            else:
                pic = printExtendInfo(IDdata[0], room_level,"3")
                await bot.send(ev, pic, at_sender=True)
    else:
        await bot.finish(ev, "查询信息输入不正确，请重新输入", at_sender=True)

@sv.on_prefix('三麻牌谱')
async def TriRecordInfo(bot, ev: CQEvent):
    nickname = ev.message.extract_plain_text()
    if len(nickname) > 15:
        sv.logger.info("昵称长度超过雀魂最大限制，已跳过")
        return
    IDdata = gettriID(nickname)
    sv.logger.info("正在查询" + nickname + "的牌谱数据")
    message = "\n"
    if IDdata == -1:
        await bot.send(ev, "没有查询到该角色在金之间以上的对局数据呢~")
    else:
        if len(IDdata) > 1:
            message = message + "查询到多条角色昵称呢~，若输出不是您想查找的昵称，请补全查询昵称\n"
            message = message + printRecordInfo(IDdata[0],3)
            await bot.send(ev, message, at_sender=True)
        else:
            message = message + printRecordInfo(IDdata[0],3)
            await bot.send(ev, message, at_sender=True)
