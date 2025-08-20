import functools
import traceback
from typing import Callable, Union, Any

from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
import os
import shutil
import asyncio
import logging

from fastapi import UploadFile


class CustomFormatter(logging.Formatter):
    def format(self, record) -> str:
        record.message = record.get_message()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


logger = None


async def setup_logger() -> Logger | Any:
    global logger
    logger = Logger(name="UIS")

    if not logger.handlers:
        current_directory = os.getcwd()
        log_path = os.path.join(current_directory, "logs/app_logger.log")
        # Настройка файлового обработчика
        rotating_handler = RotatingAsyncFileHandler(
            filename=log_path, max_bytes=20 * 1024 * 1024, backup_count=10
        )
        # Устанавливаем нужный формат для логов
        # Задайте форматирование для лога
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"  # Формат даты и времени с миллисекундами

        formatter = CustomFormatter(fmt=log_format, datefmt=date_format)

        rotating_handler.formatter = formatter
        logger.add_handler(rotating_handler)

    return logger


class RotatingAsyncFileHandler(AsyncFileHandler):
    def __init__(self, filename, max_bytes=1 * 1024 * 1024, backup_count=10, **kwargs):
        super().__init__(filename=filename, **kwargs)
        self.filename = filename
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._lock = asyncio.Lock()

    async def emit(self, record) -> None:
        async with self._lock:
            await self._rotate_logs_if_needed()
            await super().emit(record)

    async def _rotate_logs_if_needed(self) -> None:

        if (
            os.path.exists(self.filename)
            and os.path.getsize(self.filename) >= self.max_bytes
        ):
            await self._rotate_logs()

    async def _rotate_logs(self) -> None:
        # Удаляем старый самый "древний" лог (если backup_count > 0)
        if self.backup_count > 0:
            oldest_log = f"{self.filename}.{self.backup_count}"
            if os.path.exists(oldest_log):
                os.remove(oldest_log)

            # Переименовываем файлы с обратного порядка
            for i in range(self.backup_count - 1, 0, -1):
                src = f"{self.filename}.{i}"
                dst = f"{self.filename}.{i + 1}"
                if os.path.exists(src):
                    shutil.move(src, dst)

            # Переименовываем текущий лог-файл
            shutil.move(self.filename, f"{self.filename}.1")
            if not os.path.exists(self.filename):
                open(self.filename, "a").close()
            # Обновляем имя файла в обработчике
            self.stream = open(self.filename, "a")


def log_bytes_info(file: Union[UploadFile, bytes], additional_info: str = "") -> str:
    """Логирует информацию о потоке байтов или файле."""
    if isinstance(file, UploadFile):
        content_type = file.content_type
        filename = file.filename
        return f"{additional_info} File: {filename}, Content-Type: {content_type}."
    elif isinstance(file, bytes):
        file_size = len(file)
        return f"{additional_info} Bytes stream with size: {file_size} bytes"
    else:
        return f"{additional_info} Unknown file type"


def logger(func: Callable) -> Any:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        logger_log = await setup_logger()

        args_info = [
            (
                log_bytes_info(arg, additional_info="Received argument")
                if isinstance(arg, (UploadFile, bytes))
                else str(arg)
            )
            for arg in args
        ]
        kwargs_info = {
            k: (
                log_bytes_info(v, additional_info="Received keyword argument")
                if isinstance(v, (UploadFile, bytes))
                else v
            )
            for k, v in kwargs.items()
        }

        try:
            await logger_log.info(
                f"Вызов функции {func.__name__} с аргументами: {args_info}, ключевыми аргументами: {kwargs_info}"
            )
            result = await func(*args, **kwargs)
            await logger_log.info(f"Функция {func.__name__} вернула: {result}")
            return result
        except Exception as e:
            error_trace = traceback.format_exc()
            await logger_log.error(
                f"Ошибка в функции {func.__name__}: {str(e)}\nТрассировка: {error_trace}"
            )
            raise e

    return wrapper
