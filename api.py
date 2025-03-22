import asyncio
import uuid
from typing import Any

import aiohttp
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, abort, jsonify, request

from astrbot.api import logger


class PushAPIServer:
    def __init__(self, token: str, in_queue, out_queue):
        self.app = Quart(__name__)
        self.token = token
        self.in_queue = in_queue
        self.out_queue = out_queue
        self._setup_routes()
        self.http_session: aiohttp.ClientSession | None = None
        self._server_task: asyncio.Task | None = None

    def _setup_routes(self):
        @self.app.errorhandler(400)
        async def bad_request(e):
            return jsonify({"error": "Bad Request", "details": str(e)}), 400

        @self.app.errorhandler(403)
        async def forbidden(e):
            return jsonify({"error": "Forbidden", "details": str(e)}), 403

        @self.app.errorhandler(500)
        async def server_error(e):
            return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

        @self.app.route("/send", methods=["POST"])
        async def send_endpoint():
            auth_header = request.headers.get("Authorization")
            if not auth_header or auth_header != f"Bearer {self.token}":
                logger.warning(f"来自 {request.remote_addr} 的令牌无效")
                abort(403, description="无效令牌")

            data = await request.get_json()
            if not data:
                abort(400, description="无效的 JSON")

            required_fields = {"content", "umo"}
            if missing := required_fields - data.keys():
                abort(400, description=f"缺少字段: {missing}")

            message = {
                "message_id": data.get("message_id", str(uuid.uuid4())),
                "content": data["content"],
                "umo": data["umo"],
                "callback_url": data.get("callback_url"),
            }

            self.in_queue.put(message)
            logger.info(f"消息已排队: {message['message_id']}")

            return jsonify(
                {
                    "status": "queued",
                    "message_id": message["message_id"],
                    "queue_size": self.in_queue.qsize(),
                }
            )

        @self.app.route("/health", methods=["GET"])
        async def health_check():
            return jsonify(
                {
                    "status": "ok",
                    "queue_size": self.in_queue.qsize(),
                }
            )

    async def _wait_for_result(self, message_id: str) -> dict[str, Any]:
        """等待主进程处理结果"""
        while True:
            result = self.out_queue.get()
            if result.get("message_id") == message_id:
                return result
            self.out_queue.put(result)

    async def start(self, host: str, port: int):
        """启动HTTP服务"""
        self.http_session = aiohttp.ClientSession()
        config = Config()
        config.bind = [f"{host}:{port}"]
        self._server_task = asyncio.create_task(serve(self.app, config))
        logger.info(f"PushLite服务已启动于 {host}:{port}")

        try:
            await self._server_task
        except asyncio.CancelledError:
            logger.info("请求关闭服务")
        finally:
            await self.close()

    async def close(self):
        """关闭资源"""
        if self.http_session:
            await self.http_session.close()
        if self._server_task:
            self._server_task.cancel()
            try:
                await self._server_task
            except asyncio.CancelledError:
                pass


def run_server(token: str, host: str, port: int, in_queue, out_queue):
    """子进程入口"""
    server = PushAPIServer(token, in_queue, out_queue)
    asyncio.run(server.start(host, port))
