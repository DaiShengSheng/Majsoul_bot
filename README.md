<p align="center">
  <a href="https://github.com/KimigaiiWuyi/GenshinUID/"><img src="https://s2.loli.net/2022/05/20/SNaol8TUYMXLAwW.png" width="256" height="256" alt="GenshinUID"></a>
</p>
<h1 align = "center">Majsoul_bot</h1>
<h4 align = "center">✨ 基于<a href="https://github.com/Ice-Cirno/HoshinoBot" target="_blank">HoshinoBot V2</a>的雀魂Majsoul多功能插件✨ </h4>
<div align = "center">
        <a href="https://github.com/DaiShengSheng/Majsoul_bot/wiki" target="_blank">说明文档</a> &nbsp; · &nbsp;
        <a href="https://github.com/DaiShengSheng/Majsoul_bot/wiki#%E4%B8%A8%E6%8C%87%E4%BB%A4%E5%88%97%E8%A1%A8" target="_blank">指令列表</a> &nbsp; · &nbsp;
        <a href="https://github.com/DaiShengSheng/Majsoul_bot/wiki#%E4%B8%A8%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98-qa">常见问题</a>
</div>
<h4 align = "center"></h4>
<div align="center">
  <a href="https://github.com/DaiShengSheng/Majsoul_bot">
    <img src="https://img.shields.io/badge/python-3.8%2B-yellow">
  </a>
  <a href="https://github.com/Mrs4s/go-cqhttp">
    <img src="https://img.shields.io/badge/go--cqhttp-1.0.0-red">
  </a>
   <a href="https://github.com/Ice-Cirno/HoshinoBot">
    <img src="https://img.shields.io/badge/HoshinoBot-V2.0.0-green">
  </a>
  <a href="https://github.com/DaiShengSheng/Majsoul_bot/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-AGPL--3.0-blue">
  </a>
</div>

## **丨前言&插件简介**
一个雀魂信息查询 Bot 插件，该插件不包括本体，应该配合[**HoshinoBot**](https://github.com/Ice-Cirno/HoshinoBot)并结合[**go-cqhttp**](https://github.com/Mrs4s/go-cqhttp)使用：

项目地址：https://github.com/DaiShengSheng/Majsoul_bot

本插件数据来源于雀魂牌谱屋:https://amae-koromo.sapk.ch/

由于牌谱屋不收录铜之间以及银之间牌谱，故所有数据仅统计**2019年11月29日后**金场及以上场次的数据

这个项目使用的**HoshinoBot**的消息触发器，如果你了解其他QQ机器人框架的api(比如nonebot)可以只修改消息触发器就将本项目移植到其他框架

移植后转载及发布请标注本项目原地址，谢谢。

## 丨安装方法
下面介绍HoshinoBot的安装方法

1. 在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
```
git clone https://github.com/Daishengsheng/Majsoul_bot.git
```
2. 然后使用如下命令安装依赖
```
pip install -r requirements.txt
```
3. 然后在 HoshinoBot\\hoshino\\config\\\__bot__.py 文件的 MODULES_ON 加入 Majsoul_bot
4. 重启 HoshinoBot，进入机器人在的群聊，即可正常使用本插件。

## 丨已实现的功能列表
### 丨战绩查询&订阅模块
_基于雀魂牌谱屋提供的 API_
* 金之间以上的个人总体数据查询（包括总体对局信息、南场/东场个人的对局信息、放铳率、位次等）
* 个人特定段位场的总体详细数数据查询（如个人在金之间/玉之间对局的的详细信息）
* 金之间以上的个人牌谱查询（可查询近期个人最近五场的对局牌谱信息）
* 对局信息订阅与播报（基于牌谱屋对绑定的昵称进行对局监控）
### 丨其他功能模块
* 雀魂卡池的模拟抽卡（支持切换联动UP池）
* 麻将猜手牌（麻兜，代码源自[**艾琳佬的插件**](https://github.com/yuyumoko/mahjong-hand-guess)）

## 丨效果演示
### 基本数据查询
![基本数据查询](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/selectBasicInfo.png) 
### 详细数据查询
![详细数据查询](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/selectExtendInfo.png) 
### 近期对局查询
![近期对局查询](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/selectRecord.png) 
### 雀魂对局订阅
![雀魂对局订阅](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/OrderRecord.png)
### 订阅的开启与删除
![订阅的开启与删除](https://github.com/DaiShengSheng/Majsoul_bot/blob/master/screenshot/ControlRecord.png)

## 丨常见问题 Q&A
### 丨为何 Bot 启动时，报错类似No module named 'xxxxx'？
依赖未安装，使用命令pip install xxxxx即可.

若无效可尝试pip3 install xxxxx或者pip39 install xxxxx
### 丨为何我对局结束后 Bot 没有播报我的对局？
由于本插件使用的是牌谱屋的API，雀魂牌谱屋获取对局信息存在延迟，等待片刻即可。
### 丨为何查询不到我的个人信息？
由于牌谱屋只统计金之间以上的数据，请务必在查询或者订阅前在金之间对局一次，然后等待牌谱屋更新。

若还没有获取到相应信息，请再次进行查询。如果尝试几次都无法正常查询，请检查控制台后将报错截图提交到在issues当中

## | 感谢
- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ：cqhttp的golang实现，轻量、原生跨平台.  
- [Ice-Cirno / HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot) ：绝赞的QQ机器人HoshinoBot.  
- [SAPikachu / amae-koromo](https://github.com/SAPikachu/amae-koromo) ：雀魂牌谱屋！本插件查询功能API来源于此.  
- [yuyumoko / mahjong-hand-guess](https://github.com/yuyumoko/mahjong-hand-guess) ：麻兜功能小游戏.  
