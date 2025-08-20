import time
import traceback
from typing import Any
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse



class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next) -> Any:
        """
        Мидлварь, который ловит все исключения и возвращает json-ответ
        со статусом и текстом ошибки.
        """
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse({"error": str(e)}, status_code=e.status_code)
        except Exception as e:
            return JSONResponse({"code": "ERROR", "errorText": str(e)}, status_code=500)


class LogBuffer:
    """Класс для хранения логов, которые будут записаны в файл по завершению метода."""

    def __init__(self):
        self.logs = []

    def add_log(self, level, message):
        self.logs.append((level, message))

    def clear(self):
        self.logs = []


async def log_to_file(logger, logs) -> None:
    """Асинхронная запись всех логов в файл одним вызовом."""
    for log in logs:
        if log[0] == "info":
            await logger.info(log[1])
        else:
            await logger.error(log[1])


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        """
        Мидлварь, который логирует запросы.
        :param request:
        :param call_next:
        :return:
        """
        from src.setup_logger import logger

        log_buffer = LogBuffer()
        start_time = time.time()

        # Логирование информации о запросе
        log_buffer.add_log("info", f"Request received: {request.method} {request.url}")
        log_buffer.add_log("info", f"Request headers: {dict(request.headers)}")

        # Если тело запроса не пустое, логируем его
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
                log_buffer.add_log("info", f"Request body: {body}")
            except Exception as e:
                log_buffer.add_log("error", f"Error reading request body: {str(e)}")

        try:
            # Выполнение эндпоинта
            response = await call_next(request)

            # Логируем успешный ответ
            log_buffer.add_log("info", f"Response status: {response.status_code}")

            if (
                isinstance(response, StreamingResponse)
                and request.url.path != "/api/v3/ftpNotifications"
            ):
                body = b""

                async for chunk in response.body_iterator:
                    body += chunk
                # После того как мы собрали содержимое, его можно логировать
                log_buffer.add_log(
                    "info",
                    f"Streaming Response body: {body.decode('utf-8', errors='ignore')}",
                )

                # Заново создаем StreamingResponse с оригинальным содержимым
                response = StreamingResponse(
                    content=iter([body]),
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )

        except Exception as e:
            error_trace = traceback.format_exc()
            log_buffer.add_log("error", f"Ошибка:\n {error_trace}")
            raise
        finally:
            execution_time = time.time() - start_time
            log_buffer.add_log(
                "info", f"Request completed in {execution_time:.4f} seconds\n\n"
            )
            # Запись логов в конце выполнения запроса
            await log_to_file(logger, log_buffer.logs)
            log_buffer.clear()

        return response
