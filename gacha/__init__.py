from hoshino import Service, priv, MessageSegment
from hoshino.typing import HoshinoBot,CQEvent
from .gacha import *
sv = Service("雀魂抽卡")


@sv.on_fullmatch('雀魂十连')
async def majsoul_gacha(bot, ev: CQEvent):
    img = run_gacha()
    await bot.send(ev, mes + MessageSegment.image(img), at_sender=True)