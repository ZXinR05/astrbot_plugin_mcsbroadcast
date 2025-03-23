import asyncio
import secrets
from multiprocessing import Process, Queue
from typing import Any

import aiohttp

from astrbot.api import logger
from astrbot.api.star import Context, Star, register
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.message.message_event_result import MessageChain

from .api import run_server  # type: ignore


@register("astrbot_plugin_push_lite", "Raven95676", "Astrbot轻量级推送插件", "0.1.0")
class PushLite(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.in_queue: Queue | None = None
        self.process: Process | None = None
        self._running = False

    async def initialize(self):
        """初始化插件"""
        if not self.config["api"].get("token"):
            self.config["api"]["token"] = secrets.token_urlsafe(32)
            self.config.save_config()

        self.in_queue = Queue()
        self.process = Process(
            target=run_server,
            args=(
                self.config["api"]["token"],
                self.config["api"].get("host", "0.0.0.0"),
                self.config["api"].get("port", 9966),
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
            try:
                message = await asyncio.get_event_loop().run_in_executor(
                    None, self.in_queue.get
                )
                logger.info(f"正在处理消息: {message['message_id']}")

                try:
                    chain = MessageChain().message(message["content"])
                    await self.context.send_message(message["umo"], chain)
                    result = {
                        "message_id": message["message_id"],
                        "success": True,
                    }
                except Exception as e:
                    result = {
                        "message_id": message["message_id"],
                        "success": False,
                        "error": str(e),
                    }
                    logger.error(f"消息发送失败: {str(e)}")

                if callback_url := message.get("callback_url"):
                    await self._send_callback(callback_url, result)

            except Exception as e:
                logger.error(f"消息处理失败: {str(e)}")

    async def _send_callback(self, url: str, data: dict[str, Any]):
        """发送回调通知"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=5) as resp:
                    if resp.status >= 400:
                        logger.warning(f"回调失败: 状态码 {resp.status}")
        except Exception as e:
            logger.error(f"回调错误: {str(e)}")

    async def terminate(self):
        """停止插件"""
        self._running = False
        if self.process:
            self.process.terminate()
            self.process.join(5)
        if self.in_queue:
            while not self.in_queue.empty():
                self.in_queue.get()
