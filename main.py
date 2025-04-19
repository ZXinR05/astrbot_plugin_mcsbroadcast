import asyncio
import base64
import secrets
from io import BytesIO
from multiprocessing import Process, Queue
from typing import Any


import astrbot.core.message.components as Comp
from astrbot.api import logger
from astrbot.api.star import Context, Star, register
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.message.message_event_result import MessageChain

from .utils.api import run_server  # type: ignore


@register("astrbot_plugin_mcsbroadcast", "ZXinR05", "Minecraft服务器事件推送插件", "0.0.1")
class PushLite(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.in_queue: Queue | None = None
        self.process: Process | None = None
        self._running = False

    async def initialize(self):
        """初始化插件"""

        self.in_queue = Queue()
        self.process = Process(
            target=run_server,
            args=(
                self.config["api"].get("host", "0.0.0.0"),
                self.config["api"].get("port", 9977),
                dict(zip(self.config["mcs"].get("server"), self.config["mcs"].get("sid"))),
                self.in_queue,
            ),
            daemon=True,
        )
        self.process.start()
        self._running = True
        asyncio.create_task(self._process_messages())

    async def _process_messages(self):
        """处理来自子进程的消息"""
        while self._running:
            message = await asyncio.get_event_loop().run_in_executor(
                None, self.in_queue.get
            )
            logger.info(f"正在处理消息: {message['message_id']}")
            try:
                result = {"message_id": message["message_id"], "success": True}

                logger.debug("处理文本消息")
                chain = MessageChain(chain=[Comp.Plain(message["content"])])
                
                await self.context.send_message(message["umo"], chain)
                logger.info(f"消息处理完成: {message['message_id']}")
            except Exception as e:
                logger.error(f"消息发送失败: {str(e)}")
                result.update({"success": False, "error": str(e)})
            finally:
                if callback_url := message.get("callback_url"):
                    await self._send_callback(callback_url, result)
                message = None
                chain = None


    async def terminate(self):
        """停止插件"""
        self._running = False
        if self.process:
            self.process.terminate()
            self.process.join(5)
        if self.in_queue:
            while not self.in_queue.empty():
                self.in_queue.get()
