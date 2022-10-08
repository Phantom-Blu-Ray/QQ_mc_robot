#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: Yuri
# +-------------------------------------------------------------------

#------------------------------
# API of Python
#------------------------------
import time,hashlib,sys,os,json
from mcstatus import MinecraftServer
class bt_api:
    __BT_KEY = ''
    __BT_PANEL = ''

    #如果希望多台面板，可以在实例化对象时，将面板地址与密钥传入
    def __init__(self,bt_panel = None,bt_key = None):
        if bt_panel: 
            self.__BT_PANEL = bt_panel
            self.__BT_KEY = bt_key


    #取面板日志
    def get_status(self):
        #拼接URL地址
        url = self.__BT_PANEL + '/system?action=GetNetWork'

        #准备POST数据
        p_data = self.__get_key_data()  #取签名

        #请求面板接口
        result = self.__http_post_cookie(url,p_data)

        #解析JSON数据
        return json.loads(result)

    def get_disk(self):
        #拼接URL地址
        url = self.__BT_PANEL + '/system?action=GetDiskInfo'

        #准备POST数据
        d_data = self.__get_key_data()  #取签名

        #请求面板接口d
        result = self.__http_post_cookie(url,d_data)

        #解析JSON数据
        return json.loads(result)


    #计算MD5
    def __get_md5(self,s):
        m = hashlib.md5()
        m.update(s.encode('utf-8'))
        return m.hexdigest()

    #构造带有签名的关联数组
    def __get_key_data(self):
        now_time = int(time.time())
        p_data = {
                    'request_token':self.__get_md5(str(now_time) + '' + self.__get_md5(self.__BT_KEY)),
                    'request_time':now_time
                 }
        return p_data


    #发送POST请求并保存Cookie
    #@url 被请求的URL地址(必需)
    #@data POST参数，可以是字符串或字典(必需)
    #@timeout 超时时间默认1800秒
    #return string
    def __http_post_cookie(self,url,p_data,timeout=1800):
        cookie_file = './' + self.__get_md5(self.__BT_PANEL) + '.cookie'
        if sys.version_info[0] == 2:
            #Python2
            import urllib,urllib2,ssl,cookielib

            #创建cookie对象
            cookie_obj = cookielib.MozillaCookieJar(cookie_file)

            #加载已保存的cookie
            if os.path.exists(cookie_file):cookie_obj.load(cookie_file,ignore_discard=True,ignore_expires=True)

            ssl._create_default_https_context = ssl._create_unverified_context

            data = urllib.urlencode(p_data)
            req = urllib2.Request(url, data)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_obj))
            response = opener.open(req,timeout=timeout)

            #保存cookie
            cookie_obj.save(ignore_discard=True, ignore_expires=True)
            return response.read()
        else:
            #Python3
            import urllib.request,ssl,http.cookiejar
            cookie_obj = http.cookiejar.MozillaCookieJar(cookie_file)
            cookie_obj.save(ignore_discard=True, ignore_expires=True)
            cookie_obj.load(cookie_file,ignore_discard=True,ignore_expires=True)
            handler = urllib.request.HTTPCookieProcessor(cookie_obj)
            data = urllib.parse.urlencode(p_data).encode('utf-8')
            req = urllib.request.Request(url, data)
            opener = urllib.request.build_opener(handler)
            response = opener.open(req,timeout = timeout)
            cookie_obj.save(ignore_discard=True, ignore_expires=True)
            result = response.read()
            if type(result) == bytes: result = result.decode('utf-8')
            return result


def server_ip_check(server_name,server_ip):
    ser_name = '\n' + server_name.center(17,"-")
    try:
        player_omline = MinecraftServer.lookup(server_ip).status().players.online
        player_max = MinecraftServer.lookup(server_ip).status().players.max
        player_status = '\n' + "在线人数:{}/{}".format(player_omline,player_max)
        ip_ad = '\n' + 'IP地址:' + server_ip
        ping = round(MinecraftServer.lookup(server_ip).status().latency,3)
        server_ping = '\t'+ '延迟:{:.2f}'.format(ping)
    except:
        ser_name = ''
        ip_ad = ''
        player_status = ''
        server_ping = ''

    server_status_result = ser_name + ip_ad + player_status + server_ping

    return server_status_result

def server_status_check(group_panel,group_key,group_disk):
    #实例化宝塔API对象
    my_api = bt_api(group_panel,group_key)

    #调用get_logs方法
    r_data = my_api.get_status()
    r_disk = my_api.get_disk()

    #打印响应数据
    try:
        cpu_now = r_data['cpu'][0]
        mem_now = r_data['mem']['memRealUsed']/r_data['mem']['memTotal']*100
        disk_now = r_disk[group_disk]['size']
        load_now = int(r_data['load']['one']/r_data['load']['max']*100)
        if load_now>100:
            load_now = 100
        load_level = str()
        if load_now<=30:
            load_level = '运行流畅'
        elif (load_now>30&load_now<=70):
            load_level = '运行正常'
        elif (load_now>70&load_now<=90):
            load_level = '运行缓慢'
        elif (load_now>90&load_now<=100):
            load_level = '运行堵塞'
        
        server_data = '负载状态:{}% - <{}>'.format(load_now,load_level)+'\n'+'CPU使用率:{:.1f}%'.format(cpu_now)+'\n'+\
        "内存使用率:{:.1f}%".format(mem_now)+'\n'+'硬盘使用率:{}/{}'.format(disk_now[1],disk_now[0]) + "\n===================="
    except:
        server_data = "物理机状态未知".center(17,"=")

    # server_data = r_data
    return server_data

def status(group_id):

    #========检索数据========

    with open('data.json','r', encoding="utf-8") as f:
        data_json = json.load(f)
    try:
        group_server_list = data_json[group_id]
        group_panel = data_json["BT"][group_id]["panel"]
        group_key = data_json["BT"][group_id]["key"]
        group_disk = data_json["BT"][group_id]["disk"]
        # print(group_server_list)
    except:
        print('没有该群号信息')
        return '没有该群号信息'.center(17,"=")

    #========整合信息========

    server_status = str()

    server_status = server_status + '服务器状态查询'.center(17,"=") + '\n' + server_status_check(group_panel,group_key,group_disk)

    for each_ip in group_server_list:
        server_status = server_status + server_ip_check(each_ip['服务器名称'],each_ip['ip'])
    server_status = server_status + "\n===================="

    # print(server_status)
    return server_status