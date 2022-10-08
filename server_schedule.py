from typing import cast
import time

import nonebot
from mcstatus import MinecraftServer
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import (Bot, GroupMessageEvent, MessageEvent,
                                         PrivateMessageEvent)
from nonebot.plugin import require

import json

scheduler = require("nonebot_plugin_apscheduler").scheduler

@scheduler.scheduled_job("cron", minute = "*/1", id = "scheduled_check")
async def sch_check():
    bots = nonebot.get_bots()

    with open('data.json','r', encoding="utf-8") as f:
        data_json = json.load(f)
    
    for ser_each in data_json["scheduler_check"]:
        server_ip = ser_each["ip"]
        server_name = ser_each["server"]
        server_status = ser_each["status"]
        server_notice_group = ser_each["notice_group"]

        i = 0
        num = 0
        switch_status = False
        while(i<3):
            i+=1
            if num==0:
                time.sleep(3)   #检测间隔3秒
            try:
                ping = await MinecraftServer.lookup(server_ip).async_ping()
                ping = round(ping,3)
                player_omline = MinecraftServer.lookup(server_ip).status().players.online
                player_max = MinecraftServer.lookup(server_ip).status().players.max
                player_status = "{}/{}".format(player_omline,player_max)
                status = True
                num+=1
            except:
                ping = None
                player_status = "None"
                status = False
        if server_status:
            print_str = "Close" if num==0 else "Open"
            print(f"[{time.strftime('%H:%M:%S')}] {server_name}: Num = {print_str}")
            if num==0:
                switch_status = True
        elif status != server_status:
            switch_status = True
        if switch_status:
            server_status = status
            ser_each["status"] = server_status
            title_str = "服务器状态发生变化".center(17,"=")
            for bot in bots:
                for group_id_each in server_notice_group:
                    try:
                        await bots[bot].send_msg(
                        group_id = int(group_id_each),
                        message=(
                            f"{title_str}\n"
                            + f"时间：{time.strftime('%H:%M:%S')}\n"
                            + f"服务器名称: {server_name}\n"
                            + f"IP地址: {server_ip}\n"
                            + f"当前状态: {'运行中' if status else '已关闭'}"
                            + (f"\n在线人数: {player_status}" if status else "")
                            + "\t" + (f"延迟: {ping}" if status else "")
                            )
                        )
                    except:
                        pass
    data_str = json.dumps(data_json,indent=4,ensure_ascii=False)
    with open('data.json','w') as f:
        f.write(data_str)