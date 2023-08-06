__all__ = [
    'register_exception', 'BaseHTTPException', 'BadRequest', 'Unauthorized', 'Forbidden', 'NotFound',
    'MethodNotAllowed', 'CustomizeValidationError', 'ViewTimeout'
]

import traceback
from typing import Any, Optional, Dict
from asyncio import TimeoutError

# from aioredis import RedisError
from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.logger import logger
# from pymongo.errors import PyMongoError
from starlette import status

from app.utils.define import StatusCode


def log_message(request: Request, message: Any, error_type: Any):
    """
    日志输出
    :param error_type:
    :param request:
    :param message:
    :return:
    """

    logger.error('start error'.center(60, '*'))
    logger.error(f'{request.method} {request.url}')
    logger.error(f'error type is {error_type}')
    logger.error(f'error is {message}')
    logger.error('end error'.center(60, '*'))


class BaseHTTPException(HTTPException):
    STATUS_CODE = 400
    CODE = 40000
    MESSAGE = None

    def __init__(
            self,
            message: Any = None,
            status_code: int = None,
            code: int = None,
            headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.message = message or self.MESSAGE
        self.status_code = status_code or self.STATUS_CODE
        self.code = code or self.CODE
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, msg={self.message!r})"


class BadRequest(BaseHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    CODE = StatusCode.bad_request


class Unauthorized(BaseHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    CODE = StatusCode.unauthorized


class Forbidden(BaseHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    CODE = StatusCode.forbidden


class NotFound(BaseHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    CODE = StatusCode.not_found


class MethodNotAllowed(BaseHTTPException):
    STATUS_CODE = status.HTTP_405_METHOD_NOT_ALLOWED
    CODE = StatusCode.method_not_allowed


class ViewTimeout(BaseHTTPException):
    STATUS_CODE = status.HTTP_504_GATEWAY_TIMEOUT
    CODE = StatusCode.server_error
    MESSAGE = "服务器繁忙，访问受限"


class CustomizeValidationError(BaseHTTPException):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    CODE = StatusCode.validator_error
    MESSAGE = "参数校验失败"


def register_exception(app: FastAPI):
    """
    捕获FastApi异常
    :param app:
    :return:
    """

    @app.exception_handler(BaseHTTPException)
    async def catch_c_http_exception(request: Request, exc: BaseHTTPException):
        """
        捕获自定义异常
        :param request:
        :param exc:
        :return:
        """
        log_message(request, exc.message, str(exc.__class__))
        content = {'status_code': exc.code, 'message': exc.message, 'data': None}
        return JSONResponse(content=content, status_code=exc.status_code, headers=exc.headers)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        FastAPI HTTPException 异常
        :param request:
        :param exc:
        :return:
        """
        log_message(request, exc.detail, str(exc.__class__))
        content = {'status_code': StatusCode.bad_request, 'message': exc.detail, 'data': None}
        return JSONResponse(content=content, status_code=exc.status_code, headers=exc.headers)

    @app.exception_handler(AssertionError)
    async def assert_exception_handle(request: Request, exc: AssertionError):
        """
        Python AssertError 异常
        :param request:
        :param exc:
        :return:
        """

        exc_str = ''.join(exc.args)
        log_message(request, exc_str, str(exc.__class__))
        content = {'status_code': StatusCode.validator_error, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # @app.exception_handler(RedisError)
    # async def redis_error_exception_handle(request: Request, exc: RedisError):
    #     """
    #     RedisError 异常
    #     :param exc:
    #     :param request:
    #     :return:
    #     """
    #     exc_str = '|'.join(exc.args)
    #     log_message(request, exc_str, str(exc.__class__))
    #     content = {'status_code': StatusCode.validator_error, 'message': exc_str, 'data': None}
    #     return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # @app.exception_handler(PyMongoError)
    # async def py_mongo_error_exception_handle(request: Request, exc: PyMongoError):
    #     """
    #     PyMongoError 异常
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #
    #     exc_str = '|'.join(exc.args)
    #     log_message(request, exc_str, str(exc.__class__))
    #     content = {'status_code': StatusCode.validator_error, 'message': exc_str, 'data': None}
    #     return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        FastAPI RequestValidationError 异常
        :param request:
        :param exc:
        :return:
        """

        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        log_message(request, exc_str, str(exc.__class__))
        # content = exc.errors()
        content = {'status_code': StatusCode.validator_error, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(TimeoutError)
    async def timeout_exception_handle(request: Request, ex: TimeoutError):
        """
        TimeoutError 异常
        :param request:
        :param ex:
        :return:
        """

        exc_str = '服务器繁忙，访问受限'
        log_message(request, traceback.format_exc(), str(ex.__class__))
        content = {'status_code': StatusCode.server_error, 'message': str(exc_str), 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @app.exception_handler(Exception)
    async def exception_handle(request: Request, exc: Exception):
        """
        其他异常
        :param request:
        :param exc:
        :return:
        """
        log_message(request, traceback.format_exc(), str(exc.__class__))
        content = {'status_code': StatusCode.server_error, 'message': str(exc), 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
