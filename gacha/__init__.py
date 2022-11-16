from hoshino import Service, priv
from nonebot import MessageSegment
from hoshino.util import DailyNumberLimiter
from hoshino.typing import HoshinoBot,CQEvent
from .gacha import *

sv = Service("雀魂抽卡")
daily_limiter_10 = DailyNumberLimiter(15)



@sv.on_fullmatch('雀魂十连')
async def majsoul_gacha(bot, ev: CQEvent):
    userid = ev['user_id']
    if not daily_limiter_10.check(userid):
        await bot.send(ev, '今天已经抽了很多次啦，明天再来吧~')
        return
    img = run_gacha(ev["group_id"])
    daily_limiter_10.increase(userid)
    await bot.send(ev, MessageSegment.image(img), at_sender=True)

@sv.on_prefix('切换雀魂卡池')
async def change_gacha(bot, ev: CQEvent):
    user_input = ev.message.extract_plain_text()
    poolname = get_pool_id(user_input)
    if poolname == None:
        await bot.finish(ev, "没有找到该名称的卡池，请查看输入的卡池名称是否正确，当前支持的卡池有："
                             +"当前up池、辉夜up池、天麻up池1、天麻up池2、标配池、斗牌传说up池、狂赌up池\n（请输入 切换雀魂卡池 卡池名称 进行切换）", at_sender=True)

    group_id = ev["group_id"]
    group_pool = group_pool_loader()
    group_pool_list = []
    check_flag = 0

    for i in range(0,len(group_pool)):
        if group_pool[i]["gid"] == str(group_id):
            check_flag = 1
            binds = {
                "gid": str(group_id),
                "poolname": poolname
            }
            group_pool_list.append(binds)
        else:
            group_pool_list.append(group_pool[i])
    if check_flag == 0:
        binds = {
            "gid": str(group_id),
            "poolname": poolname
        }
        group_pool_list.append(binds)

    with open(join(path, 'group_pool.json'), 'w', encoding='utf-8') as fp:
        json.dump(group_pool_list, fp, indent=4)
    await bot.finish(ev, "已成功将本群卡池切换到：" + get_pool_name(poolname), at_sender=True)

@sv.on_fullmatch(('查看雀魂卡池','当前雀魂卡池'))
async def view_gacha(bot, ev: CQEvent):
    group_id = ev["group_id"]
    group_pool = group_pool_loader()
    group_pool_list = []
    check_flag = 0

    for i in range(0, len(group_pool)):
        if group_pool[i]["gid"] == str(group_id):
            check_flag = 1
            await bot.finish(ev, "本群启用的雀魂卡池为：" + get_pool_name(group_pool[i]["poolname"]), at_sender=True)
        group_pool_list.append(group_pool[i])
    if check_flag == 0:
        binds = {
            "gid": str(group_id),
            "poolname": "up"
        }
        group_pool_list.append(binds)
    with open(join(path, 'group_pool.json'), 'w', encoding='utf-8') as fp:
        json.dump(group_pool_list, fp, indent=4)
    await bot.finish(ev, "本群启用的雀魂卡池为：当前up池", at_sender=True)
