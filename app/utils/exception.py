import logging
import traceback
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 开发模式：返回详细错误信息
# 生产模式：返回简化错误信息
DEBUG_MODE = True


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    处理 HTTPException 异常（业务主动抛出）
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    处理请求参数校验错误 (Pydantic / FastAPI 自动校验)
    """
    errors = exc.errors()
    # 提取第一条参数错误提示
    error_msg = f"参数校验错误: {errors[0]['loc'][-1]} {errors[0]['msg']}" if errors else "请求参数格式错误"

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,  # 或 HTTP_422_UNPROCESSABLE_ENTITY
        content={
            "code": 400,
            "message": error_msg,
            "data": errors if DEBUG_MODE else None
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    处理数据库完整性约束错误
    """
    error_msg = str(exc.orig)

    # 判断具体的约束错误类型
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"

    # 记录 Warning 日志
    logger.warning(f"数据约束冲突: {request.url.path} - {error_msg}")

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url)
        }

    return JSONResponse(
        # 推荐使用 409 Conflict 替代 400
        status_code=status.HTTP_409_CONFLICT,
        content={
            "code": 409,
            "message": detail,
            "data": error_data
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    处理 SQLAlchemy 数据库通用错误
    """
    # 发生数据库异常，生产环境中必须记录堆栈日志！
    logger.error(f"数据库执行异常: {request.url.path}", exc_info=True)

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后重试",
            "data": error_data
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    处理所有未捕获的系统致命异常
    """
    # 关键：记录全局堆栈日志
    logger.critical(f"系统未捕获致命异常: {request.url.path}", exc_info=True)

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": error_data
        }
    )