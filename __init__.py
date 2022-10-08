import time
from turtle import title
from nonebot import get_driver, on_message, on_notice
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
import random
from nonebot.rule import Rule
from datetime import date
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import MessageSegment,Message,GroupMessageEvent,PrivateMessageEvent,MessageEvent
from nonebot.permission import SUPERUSER
from nonebot import require
from nonebot import get_driver
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
require("nonebot_plugin_apscheduler")

import time
from .server_status import status


from nonebot_plugin_apscheduler import scheduler

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

rnd = random.Random()

#--------文件设定-----------#
Version_No = "2.1.1"
clear_minute = str(int(random.random()*10)+48)
clear_hour = "23"
notice_minute = str(int(random.random()*10)+1)
notice_hour = "9,10,11,12,15,16,17,18"
random_time = (int(random.random()*10)+1)/10
#--------------------------#



#-------------------随机时间函数-------------------#

def random_num():
    rnd.seed(int(date.today().strftime("%Y%m%d%H%M%S%W%j")))
    return rnd.randint(0,1)

def random_time_num():
    return int(random_num()*10)/10

def clear_minute_num():
    return str(int(random_num()*10)+48)

def notice_minute_num():
    return str(int(random_num()*10))

#-------------------------------------------------#

startup_driver = get_driver()


# async def user_checker(event: Event) -> bool:
#     return event.get_user_id() == "1615684646"  #匹配超管QQ

# rule = Rule(user_checker)  #整合多个匹配规则

# hello = on_message(rule=rule,priority=10)
# @hello.handle()
# async def hello_handle(bot: Bot, event: Event):
#     await hello.finish(Message(f'事件类型:{event.get_type}'))


#-------------------------------------------------#




#--------群组检测阻断-------#

# bot_checker = on_message(priority=13,block=False) # block=False 即默认不阻断事件
# @bot_checker.handle()
# async def hello_handle(matcher: Matcher, event: GroupMessageEvent):
#     if event.group_id != 754249043:
#         matcher.stop_propagation()

#--------------------------#



#-------服务器状态检测------#

mc_status = on_command("服务器状态",priority=6) # block=False 即默认不阻断事件
@mc_status.handle()
async def mc_sever_status(bot:Bot,event:GroupMessageEvent):
    group_id: str = str(event.group_id)
    mc_status_str = status(group_id)
    await bot.send_group_msg(group_id=group_id,message=Message(mc_status_str),auto_escape=False)

#--------------------------#



#--------指令设定-----------#

command_test = on_command("测试",permission=SUPERUSER,priority=18)
@command_test.handle()
async def command_testcheck(bot:Bot,event:MessageEvent):
    if isinstance(event, GroupMessageEvent):
        time.sleep(random_time_num())
        try:
            group_id: str = str(event.group_id)
            str_command = f"""<<<<<机器人在线>>>>>
[CQ:face,id=168]robot-Version-{Version_No}
[CQ:face,id=168]指令正常
[CQ:face,id=168]状态正常"""
            await bot.send_group_msg(group_id=group_id,message=Message(str_command),auto_escape=False)
        except AttributeError:
            pass

command_list = on_command("指令列表",priority=20)
@command_list.handle()
async def command_tips(bot:Bot,event:MessageEvent):
    if isinstance(event, GroupMessageEvent):
        time.sleep(random_time_num())
        try:
            group_id: str = str(event.group_id)
            title_str = "所有指令之前均需要打\"/\"".center(23,"=")
            str_command = f"""{title_str}
[CQ:face,id=54]管理员指令 | [CQ:face,id=168]群成员指令
[CQ:face,id=54]测试机器人状态：测试
[CQ:face,id=54]查询机器人状态：状态
[CQ:face,id=168]查看指令列表：指令列表
[CQ:face,id=168]查询服务器状态：服务器状态
[CQ:face,id=168]服务器状态变化时进行提醒"""
            await bot.send_group_msg(group_id=group_id,message=Message(str_command),auto_escape=False)
        except AttributeError:
            pass

#--------------------------#



#-------------------启动操作函数-------------------#

# @startup_driver.on_bot_connect
# async def check_lastdata(bot: Bot):
#     @scheduler.scheduled_job("cron", hour = clear_hour,minute = clear_minute_num(), id="file_date_2")
#     async def msg_clear():
#         await bot.send_group_msg(group_id=set_group_id,message=Message(f"[{time.strftime('%H:%M:%S')}]"),auto_escape=False)

#-------------------------------------------------#