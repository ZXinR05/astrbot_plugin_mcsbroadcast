**注意：** 本插件还在开发初期阶段

# 简介

Minecraft 服务器事件推送
本插件是一个基于 [astrbot_plugin_push_lite](https://github.com/Raven95676/astrbot_plugin_push_lite)修改而来的项目

可以推送玩家进出服务器信息、死亡信息、游戏内聊天信息等

# 准备工作

-   确保 Astrbot 安装的机器能被公网访问，或 Astrbot 安装在与 Minecraft 服务端同一局域网内
-   安装好 Astrbot 插件
-   使用 PaperMC 服务端，安装[WebhookTool](https://github.com/ZXinR05/WebhookTool)插件

# 配置

1.启动 MC 服务端首次加载 API 插件  
2.停止 MC 服务端  
3.编辑`/plugins/WebhookTool/config.yml`

-   `urls`内改成`- http://IP:Port/send`, `IP`为 Astrbot 所在的机器 IP, `Port`为 API 监听端口
-   `webhook_token`内填入自定义字符串，如:`webhook_token: mytoken123`
-   去除`urls`内多余的地址

4.打开 Astrbot 插件配置, 在`token`内填入与`webhook_token`一致的字符串, 在`sid`内填入聊天的`sid`, **(若有多个 token 请与 sid 一一对应)**  
5.编辑`/plugins/WebhookTool/config.yml`文件, 选择开启或关闭某些事件播报

# 支持

[Astrbot](https://astrbot.app)  
[astrbot_plugin_push_lite](https://github.com/Raven95676/astrbot_plugin_push_lite)  
[MinecraftServerAPI](https://github.com/Shweit/MinecraftServerAPI)  
[WebhookTool](https://github.com/ZXinR05/WebhookTool)
