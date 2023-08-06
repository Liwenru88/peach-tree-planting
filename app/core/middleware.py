__all__ = [
    'register_cross', 'register_middleware', 'register_startup_and_shutdown'
]

import asyncio
import datetime
import logging
import time

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse

from app.core import config
from app.core.app_context import app_ctx
from app.core.config import settings
from app.core.exception import ViewTimeout
from app.core.log import request_id_generator, request_id_var

logger = logging.getLogger(__name__)


class TimeoutMiddleware:
    """视图函数运行超时拦截"""

    def __init__(self, app: FastAPI, timeout: float, whitelist: list[str]):
        self.app = app
        self.timeout = timeout
        self.whitelist = whitelist

    async def __call__(self, request: Request, call_next):
        if request.url.path in self.whitelist:
            return await call_next(request)
        try:
            response = await asyncio.wait_for(call_next(request), timeout=self.timeout)
            return response
        except asyncio.TimeoutError:
            exc = ViewTimeout()
            content = {'status_code': exc.code, 'message': exc.message, 'data': None}
            return JSONResponse(content=content, status_code=exc.status_code, headers=exc.headers)


def register_cross(app: FastAPI):
    """
    跨越配置
    :param app:
    :return:
    """
    origins = settings.BACKEND_CORS_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def rewrite_other_exception_response(request: Request, call_next):
        """
        中间件
        :param request:
        :param call_next:
        :return:
        """
        start_time = time.time()

        # 生成request_id
        if header_value := request.headers.get("x-request-id"):
            request_id = header_value
        else:
            request_id = request_id_generator()
        # 设置request_id
        request_id_var.set(request_id)
        if settings.DEV_ENV and (request.url.path.startswith("/oauth2/mp")
                                 or request.url.path.startswith("/openapi/mp")):
            # 测试环境下转Mock
            response = RedirectResponse(
                f"/mock{request.url.path}?{request.query_params}", headers={"X-Response-From": "Mock"}
            )
            response.headers["X-Response-From"] = "Mock"
            return response

        response = await call_next(request)

        process_time = time.time() - start_time
        # 无nginx
        ip = request.client.host
        # 有Nginx  二选一 得看NGINX 的配置
        ip = request.headers.get('X-Real-IP')
        # 因为有可能走多层代理 取最后一个
        if not ip:
            ip = request.client.host

        ip = ip.split(',')[-1]
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        path = request.url
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        logger.info(f"{time_str} | {ip} | {path}：处理时间：{process_time}s")
        return response

    # timeout_middleware = TimeoutMiddleware(app, timeout=10.0, whitelist=[])
    # app.middleware("http")(timeout_middleware)


def register_startup_and_shutdown(app: FastAPI) -> None:
    """
    服务启动和结束事件
    :param app:
    :return:
    """

    @app.on_event('startup')
    async def startup_event():
        """
        启动
        :return:
        """
        await app_ctx.init_app()

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        关闭
        :return:
        """
        await app_ctx.close()
