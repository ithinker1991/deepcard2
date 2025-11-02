"""
日志配置模块
"""
import logging
import sys
from typing import Dict, Any
from pathlib import Path

from app.shared.config import get_settings


def setup_logging() -> None:
    """配置应用日志"""
    settings = get_settings()

    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 根日志器配置
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # 清除现有处理器
    root_logger.handlers.clear()

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 文件处理器（仅在非调试模式下）
    if not settings.DEBUG:
        file_handler = logging.FileHandler(log_dir / "app.log", encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # 错误日志文件
        error_handler = logging.FileHandler(log_dir / "error.log", encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        root_logger.addHandler(error_handler)


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志器"""
    return logging.getLogger(name)


# API请求日志装饰器
def log_api_call(func):
    """API调用日志装饰器"""
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)

        # 记录请求开始
        logger.info(f"API调用开始: {func.__name__}")

        try:
            result = await func(*args, **kwargs)
            logger.info(f"API调用成功: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"API调用失败: {func.__name__} - {str(e)}", exc_info=True)
            raise

    return wrapper


# 数据库操作日志装饰器
def log_db_operation(operation: str):
    """数据库操作日志装饰器"""
    def decorator(func):
        import functools

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)

            # 记录数据库操作开始
            logger.debug(f"数据库操作开始: {operation}")

            try:
                result = await func(*args, **kwargs)
                logger.debug(f"数据库操作成功: {operation}")
                return result
            except Exception as e:
                logger.error(f"数据库操作失败: {operation} - {str(e)}", exc_info=True)
                raise

        return wrapper
    return decorator


# LLM调用日志装饰器
def log_llm_call(provider: str, model: str):
    """LLM调用日志装饰器"""
    def decorator(func):
        import functools

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)

            # 记录LLM调用开始
            logger.info(f"LLM调用开始: provider={provider}, model={model}")

            try:
                result = await func(*args, **kwargs)
                logger.info(f"LLM调用成功: provider={provider}, model={model}")
                return result
            except Exception as e:
                logger.error(f"LLM调用失败: provider={provider}, model={model} - {str(e)}", exc_info=True)
                raise

        return wrapper
    return decorator


# 性能监控装饰器
def log_performance(operation: str):
    """性能监控日志装饰器"""
    import functools
    import time

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)

        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"操作完成: {operation}, 耗时: {duration:.3f}秒")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"操作失败: {operation}, 耗时: {duration:.3f}秒 - {str(e)}", exc_info=True)
            raise

    return wrapper


# 用户操作审计日志
def audit_user_action(user_id: str, action: str, details: Dict[str, Any] = None):
    """记录用户操作审计日志"""
    logger = get_logger("audit")

    log_data = {
        "user_id": user_id,
        "action": action,
        "details": details or {}
    }

    logger.info(f"用户操作: {user_id} - {action} - {log_data}")


# 安全事件日志
def log_security_event(event_type: str, details: Dict[str, Any] = None):
    """记录安全事件日志"""
    logger = get_logger("security")

    log_data = {
        "event_type": event_type,
        "details": details or {}
    }

    logger.warning(f"安全事件: {event_type} - {log_data}")