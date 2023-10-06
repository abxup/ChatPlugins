import json
import websockets
import pprint
import os
import requests

group_id_global = None
data = None  # 创建一个变量来存储数据

def send_group_msg(group,message, auto_escape=False):
    url = "http://abxup.top:5700/send_group_msg"
    data = {
        "group_id": group,
        "message": message,
        "auto_escape": auto_escape
    }
    response = requests.post(url, json=data)
    response_data = response.json()
    return response_data.get("message_id")


def abxup(query_value):

    headers = {
        "Host": "chat-ws.baidu.com",
        "Cookie": "BIDUPSID=5B2279294425293679E2F5877CB74773; PSTM=1696044896; BAIDUID=5B227929442529363B6EB554E3F1A593:FG=1; BDUSS_BFESS=XpaMFpNZ25kNnhxUE9STmdBMU1OS3lwM2ZkRWJKeWJuUkdiMnJacGFrR2NKRDlsRUFBQUFBJCQAAAAAAAAAAAEAAADL14BsTnViZXJGUlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJyXF2Wclxdla; BAIDUID_BFESS=5B227929442529363B6EB554E3F1A593:FG=1; ZFY=BVfmXVf09W78cZ:AVeKCd:BJhdGsBy4h:BWy7QQsTLcxmA:C; BA_HECTOR=0ka4812k258h8h248h0k052k1ihvjmk1o; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ET_WHITELIST=etwhitelistintwodays",
        "Sec-Ch-Ua": "",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
        "Sec-Ch-Ua-Platform": "",
        "Origin": "https://www.baidu.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.baidu.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
    }

    # 请求数据
    data = {
        "message": {
            "inputMethod": "keyboard",
            "isRebuild": False,
            "lastMsgId": "",
            "lastMsgIndex": 0,
            "content": {
                "query": query_value,
                "qtype": 0,
                "customes": [],
                "botQuery": {},
                "autoQuery": False,
                "pluginQuery": {},
                "pageInfo": {},
                "containerInfo": {
                    "containerType": 0,
                    "isDegrade": 0
                },
                "pluginInfo": []
            }
        },
        "sessionId": "767bb63a-df68-4b2a-9eff-9ce720619c85",
        "aisearchId": "12461912709747405820",
        "pvId": "10154905205412717046",
        "newTopic": False
    }
    response = requests.post("https://chat-ws.baidu.com/aichat/api/conversation", headers=headers, json=data)
    
    try:
        data_lines = response.text.splitlines()
        output = [json.loads(line.split("data:")[-1].strip())['data']['message']['content']['generator']['text']
                  for line in data_lines if 'content' in line and 'generator' in line]
        return '\n'.join(output)
    except json.JSONDecodeError:
        return "Error decoding response."




async def listen():
    uri = "ws://abxup.top:8081"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)  # 将数据存储在变量中
            ## pprint.pprint(data)  # 使用pprint替代print
            
            # 检查是否存在'group_id'和'message'
            if 'group_id' in data and 'message' in data:
                if "[CQ:at,qq=3477204796]" in data['message']:
                    if 'user_id' in data:
                        group_id_global = data.get('group_id')
                        print(group_id_global)
                        message_chat = data['message'].replace("[CQ:at,qq=3477204796]", "")  # 将'message'的内容存储在message_chat变量中，同时排除"[CQ:at,qq=3477204796]"
                        
                        user_id = data['user_id']
                        print(user_id)
                        ## 构建一个消息[CQ:at,qq=user_id]+message_chat
                        message_chat =abxup(message_chat)
                        message = f"[CQ:at,qq={user_id}]{message_chat}"
                        ## 发送消息
                        send_group_msg(group_id_global,message)

# 运行监听函数
import asyncio

asyncio.run(listen())
