from hoshino import Service
from hoshino.typing import HoshinoBot,CQEvent
from .cal_mahjong import *

sv = Service("麻将牌理")

@sv.on_prefix('牌理')
async def cal_mahjong(bot, ev: CQEvent):
    hands = ev.message.extract_plain_text()
    if len(hands) == 0:
        await bot.finish(ev, "查询的麻将手牌数量不可为空" , at_sender=True)
        return
    result = calc_shanten_14(hands)
    message = ""
    if isinstance(result,str):
        await bot.finish(ev, result , at_sender=True)
        return
    else:
        for i in range (0,len(result)):
            message = message + result[i]
        pic = ImgText(message)
        await bot.finish(ev, pic.draw_text(), at_sender=True)
