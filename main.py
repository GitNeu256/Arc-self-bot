import json
import threading
import time

import websocket
import requests

# https://discord.com/api/v9/channels/758329875207159882/messages

with open("config.json") as f:
    config = json.load(f)

# Comamnds
# Default
def send_message(channel_id, message):
    header = {
        "Authorization": config["Token"]
    }

    payload = {
        "content": message
    }

    requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                data = payload, headers = header)
    
def delete_msg(channel_id, message_id):
    header = {
        "Authorization": config["Token"]
    }

    requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}",
                headers = header)

# Custom

# Logging message
def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)
 
def heartbeat(interval, ws):
    print("Heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")

if config["DebugMode"] == "True":
    websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
event = recive_json_response(ws)

heartbeat_interval = event["d"]["heartbeat_interval"]
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = config["Token"]
payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}

send_json_request(ws, payload)

while True:
    event = recive_json_response(ws)

    try:
        #print(f'{event["d"]["author"]["username"]}: {event["d"]["content"]}; {event["d"]["channel_id"]}')

        #print(event["d"]["id"])

        if event["d"]["author"]["username"] == config["UserName"]:
            message = event["d"]["content"]

            msg1 = message.split(" ")
            command = msg1.pop(0)
            msg2 = " ".join(msg1)

            command = command[1:]
            
            if command == "msg_sp_1":
                delete_msg(event["d"]["channel_id"], event["d"]["id"])
                spoler_msg = f"||{msg2}||"
                send_message(event["d"]["channel_id"], spoler_msg)
            elif command == "msg_sp_2":
                delete_msg(event["d"]["channel_id"], event["d"]["id"])
                msg_spoler = list(msg2)
                spoler_msg_list = []

                for element in msg_spoler:
                    msg_for_spoler = f"||{element}||"
                    spoler_msg_list.append(msg_for_spoler)

                spoler_msg = "".join(spoler_msg_list)

                send_message(event["d"]["channel_id"], spoler_msg)
            elif command == "img_sp":
                delete_msg(event["d"]["channel_id"], event["d"]["id"])
                
        #op_code = event("op")
        #if op_code == 11:
        #    print("heartbeat received")
    except:
        pass