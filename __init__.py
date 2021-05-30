# coding=utf-8
from hoshino import Service

sv = Service("雀魂帮助")


help_txt = '''这是一个HoshinoBot的雀魂查询相关插件
本插件数据来源于雀魂牌谱屋:https://amae-koromo.sapk.ch/
项目地址：https://github.com/DaiShengSheng/Majsoul_bot
由于牌谱屋不收录铜之间以及银之间牌谱，故所有数据仅统计2019年11月29日后金场及以上场次的数据
PS：本插件暂时只支持四麻对局的查询，后续会完善三麻查询功能

查询指令：
雀魂信息/雀魂查询 昵称：查询该ID的雀魂基本对局数据(包含金场以上所有)
雀魂信息/雀魂查询 (金/金之间/金场/玉/王座) 昵称：查询该ID在金/玉/王座之间的详细数据
雀魂牌谱 昵称：查询该ID下最近五场的对局信息

对局订阅指令：
雀魂订阅 昵称：订阅该昵称在金之间以上的四麻对局信息 
(取消/关闭)雀魂订阅 昵称：将该昵称在本群的订阅暂时关闭 
开启雀魂订阅 昵称：将该昵称在本群的订阅开启 
删除雀魂订阅 昵称：将该昵称在本群的订阅删除
雀魂订阅状态：查询本群的雀魂订阅信息的开启状态 
'''

@sv.on_fullmatch("雀魂帮助")
async def help(bot, ev):
    await bot.send(ev, help_txt)

