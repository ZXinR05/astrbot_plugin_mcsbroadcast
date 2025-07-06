import uuid


def event_handel(data, sid):
    message = {
        "message_id": data.get("message_id", str(uuid.uuid4())),
        "content": data["message"],
        "umo": sid,
        "type": "text",
    }
    event = data["event"]


    if event == "player_quit":
        message["content"] = f'{data["message"]} 在线时长 {data["duration"]}'
        
    if event == "player_chat":
        message["content"] = fr'{data["player"]}: {data["message"]}'

    return message



