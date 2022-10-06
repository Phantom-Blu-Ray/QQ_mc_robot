from server_status import status,server_status_check,server_ip_check

# print(status("656783128"))
print(server_ip_check("启示录","sq.s1.vlssu.com:44013"))
# print(server_status_check("http://211.101.244.74:8888","QjakSI95NXe1soqn8vhNpnM85goxtW8V",1))

# import json

# with open('data.json','r', encoding="utf-8") as f:
#     data_json = json.load(f)
#     # print(f.read())
# for ser_each in data_json["scheduler_check"]:
#     server_notice_group = ser_each["notice_group"]
#     for group_id_each in server_notice_group:
#         print(group_id_each)
