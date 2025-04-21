**注意：** 本插件还在开发初期阶段
# 简介

Minecraft 服务器事件推送
本插件是一个基于 [astrbot_plugin_push_lite](https://github.com/Raven95676/astrbot_plugin_push_lite)修改而来的项目

可以推送玩家进出服务器信息、死亡信息、游戏内聊天信息等

# 准备工作
* 确保Astrbot安装的机器能被公网访问，或Astrbot安装在与Minecraft服务端同一局域网内
* 安装好Astrbot插件
* 使用Spigot、PaperMC等可装插件的服务端，安装[MinecraftServerAPI](https://github.com/Shweit/MinecraftServerAPI)插件
# 配置
  1.启动MC服务端首次加载API插件
  2.停止MC服务端
  3.编辑`/plugins/MinecraftServerAPI/config.yml`, 在25行`urls`内改成`- http://IP:9977/send`, IP为Astrbot所在的机器IP
  4.去除`urls`内多余的地址
  5.打开Astrbot插件配置, 在`server`内填入Minecraft服务器的**IP** *注意不要填域名*, 在`sid`内填入聊天的`sid`, **(若有多个服务器请与sid一一对应)**  
  **如果使用了frp等端口转发工具, `server`内请填写中转服务器的IP**
  6.编辑`/plugins/MinecraftServerAPI/config.yml`文件, 选择开启或关闭某些事件播报
# 使用
  * 事件适配情况 ~~(后期可能会更新事件触发自定义文字功能)~~
  | 事件                    | 适配 |
|-------------------------|------|
| server_start            | ✓    |
| server_stop             | ✓    |
| plugin_disable          | ✗    |
| plugin_enable           | ✗    |
| block_break             | ✗    |
| block_place             | ✗    |
| block_burn              | ✗    |
| block_redstone          | ✗    |
| note_play               | ✗    |
| sign_change             | ✗    |
| enchant_item            | ✗    |
| creeper_power           | ✗    |
| creature_spawn          | ✗    |
| entity_death            | ✗    |
| entity_explode          | ✗    |
| entity_shoot_bow        | ✗    |
| entity_tame             | ✗    |
| explosion_prime         | ✗    |
| player_death            | ✓    |
| brew                    | ✗    |
| craft_item              | ✗    |
| furnace_burn            | ✗    |
| furnace_smelt           | ✗    |
| player_chat             | ✓    |
| player_login            | ✓    |
| player_command          | ✗    |
| player_gamemode_change  | ✗    |
| player_item_break       | ✗    |
| player_join             | ✓    |
| player_kick             | ✓    |
| player_quit             | ✓    |
| player_respawn          | ✓    |
| lightning_strike        | ✗    |
| weather_change          | ✓    |
| thunder_change          | ✗    |
| world_load              | ✗    |
| world_save              | ✗    |
| world_unload            | ✗    |

# 支持
[Astrbot](https://astrbot.app)  
[astrbot_plugin_push_lite](https://github.com/Raven95676/astrbot_plugin_push_lite)  
[MinecraftServerAPI](https://github.com/Shweit/MinecraftServerAPI)
