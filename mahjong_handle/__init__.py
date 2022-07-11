from hoshino import Service, priv
from nonebot import MessageSegment
from .handler import HandGuess
from .utils import get_path

sv_help = """
[麻将猜手牌/开启麻兜] 开始一轮猜测当前手牌游戏
""".strip()

sv = Service(
    name="麻兜",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="娱乐",  # 分组归类
    help_=sv_help,  # 帮助说明
)


@sv.on_fullmatch(("麻将猜手牌","开启麻兜"))
async def main(bot, ev):

    hg = HandGuess(ev["user_id"], ev["group_id"])
    res = await hg.start()
    if res["error"]:
        await bot.finish(ev, res["msg"])
    await bot.send(ev, f"开始一轮猜手牌, 每个人有{hg.MAX_GUESS}次机会")

    rule_path = get_path("assets", "rule.png")
    await bot.send(ev, MessageSegment.image(f"file:///{rule_path}"))

@sv.on_fullmatch(("结束猜手牌","结束麻兜"))
async def end_game(bot, ev):
    hg = HandGuess(ev["user_id"], ev["group_id"])
    res = await hg.end_game()

@sv.on_message("group")
async def on_input_chara_name(bot, ev):
    msg = ev["raw_message"]
    hg = HandGuess(ev["user_id"], ev["group_id"])

    if hg.is_start():
        res = await hg.guesses_handler(msg)
        if res.get("img"):
            await bot.send(ev, MessageSegment.image(res["img"]), at_sender=True)

        if res.get("msg"):
            await bot.send(ev, res["msg"], at_sender=True)
