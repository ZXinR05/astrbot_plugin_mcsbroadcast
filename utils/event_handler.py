import uuid


def event_handel(data, sid):
    message = {
        "message_id": data.get("message_id", str(uuid.uuid4())),
        "content": data["event"],
        "umo": sid,
        "type": "text",
    }
    event = data["event"]
    if event == "player_death":
        message["content"] = f'{data.get("player")}死了:{data.get("cause")}'

    if event == "player_chat":
        message["content"] = f'{data.get("player")}说:{data.get("message")}'

    if event == "server_start":
        message["content"] = "服务器已启动"

    if event == "server_stop":
        message["content"] = "服务器已关闭"
    
    if event == "player_login":
        message["content"] = f'{data.get("player")}加入了游戏'

    if event == "player_quit":
        message["content"] = f'{data.get("player")}退出了游戏'

    if event == "player_respawn":
        message["content"] = f'{data.get("player")}重生了'

    if event == "weather_change":
        message["content"] = "我的世界下雨了" if data.get("rain") else "我的世界又不下雨了"

    return message



