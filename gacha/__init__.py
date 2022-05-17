from hoshino import Service, priv, MessageSegment
from hoshino.typing import HoshinoBot,CQEvent
from hoshino.util import DailyNumberLimiter
from .gacha import *

sv = Service("雀魂抽卡")
daily_limiter_10 = DailyNumberLimiter(10)

@sv.on_fullmatch('雀魂十连')
async def majsoul_gacha(bot, ev: CQEvent):
    userid = ev['user_id']
    if not daily_limiter_10.check(userid):
        await bot.send(ev, '今天已经抽了很多次啦，明天再来吧~')
        return
    img = run_gacha()
    daily_limiter_10.increase(userid)
    await bot.send(ev, mes + MessageSegment.image(img), at_sender=True)
