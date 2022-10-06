import json
from mcstatus import MinecraftServer

def server_ip_check(server_name,server_ip):
    ser_name = '\n' + "---" + server_name + "---"
    try:
        player_omline = MinecraftServer.lookup(server_ip).status().players.online
        player_max = MinecraftServer.lookup(server_ip).status().players.max
        player_status = '\n' + "在线人数:{}/{}".format(player_omline,player_max)
        ip_ad = '\n' + 'IP地址:' + server_ip
        ping = MinecraftServer.lookup(server_ip).status().latency
        server_ping = '\t'+ '延迟:{:.2f}'.format(ping)
    except:
        ser_name = ''
        ip_ad = ''
        player_status = ''
        server_ping = ''

    server_status_result = ser_name + ip_ad + player_status + server_ping

    return server_status_result

# group_id = '276650538'
group_id = '656783128'

with open('data.json','r', encoding="utf-8") as f:
    data_json = json.load(f)
try:
    group_server_list = data_json[group_id]
    # print(group_server_list)
except:
    print('没有该群号信息')

server_status = str()

if group_id == '754249043':
    server_status = "====服务器状态查询===="

for each_ip in group_server_list:
    server_status = server_status + server_ip_check(each_ip['服务器名称'],each_ip['ip'])
server_status = server_status + "\n======================"

print(server_status)