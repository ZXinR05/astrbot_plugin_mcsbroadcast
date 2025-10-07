import asyncio
import uuid

from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, abort, jsonify, request

from astrbot.api import logger
from .event_handler import event_handel


class PushAPIServer:
    def __init__(self, pair: dict, in_queue):
        self.app = Quart(__name__)
        self.pair = pair
        self.in_queue = in_queue
        self._setup_routes()
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
            source = request.remote_addr
            data = await request.get_json()
            token = request.headers.get("X-Webhook-Token")
            
            if not data:
                logger.warning("无效的 JSON")
                abort(400, description="无效的 JSON")
            
            if not self.pair.get(token):
                # logger.warning(f"{request.remote_addr} 不在服务器列表中")
                abort(400, description="不在服务器列表中")
            logger.debug(f"收到来自{source}的消息：{data}")

            required_fields = {"event"}
            if missing := required_fields - data.keys():
                logger.warning(f"缺少字段: {missing}")
                abort(400, description=f"缺少字段: {missing}")

            message = event_handel(data, self.pair.get(token))

            self.in_queue.put(message)
            logger.info(f"消息已排队: {message['message_id']}")

            return jsonify(
                {
                    "status": "queued",
                    "message_id": message["message_id"],
                    # "queue_size": self.in_queue,
                }
            )


    async def start(self, host: str, port: int):
        """启动HTTP服务"""
        config = Config()
        config.bind = [f"{host}:{port}"]
        self._server_task = asyncio.create_task(serve(self.app, config))
        logger.info(f"MCSBroadcast服务已启动于 {host}:{port}")

        try:
            await self._server_task
        except asyncio.CancelledError:
            logger.info("请求关闭服务")
        finally:
            await self.close()

    async def close(self):
        """关闭资源"""
        if self._server_task:
            self._server_task.cancel()
            try:
                await self._server_task
            except asyncio.CancelledError:
                pass


def run_server(host: str, port: int, pair: dict, in_queue):
    """子进程入口"""
    server = PushAPIServer(pair, in_queue)
    asyncio.run(server.start(host, port))
    

