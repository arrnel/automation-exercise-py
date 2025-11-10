import inspect
import logging
from contextlib import contextmanager
from functools import wraps
from typing import Callable, TypeVar, Optional, Generator

import allure

from src.model.enum.log_level import LogLvl

T = TypeVar("T")


class SafeDict(dict):
    """Безопасный dict для .format_map — не ломается, если ключа нет."""

    def __missing__(self, key):
        return f"{{{key}}}"


class StepLogger:
    """
    Log step and add allure step:
    """

    def __init__(self, default_level: LogLvl = LogLvl.INFO):
        self.default_level = default_level

    def log(
        self, message: str, log_level: Optional[LogLvl] = None
    ) -> Callable[..., T] | Generator[None, None, None]:

        level = log_level or self.default_level

        # --- режим контекстного менеджера ---
        @contextmanager
        def _context_manager():
            logging.log(level.code, message)
            with allure.step(message):
                yield

        # --- режим декоратора ---
        def _decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                # Собираем контекст вызова
                bound_args = inspect.signature(func).bind_partial(*args, **kwargs)
                bound_args.apply_defaults()

                context = SafeDict(bound_args.arguments)

                # Если есть self — добавляем его атрибуты
                self_obj = context.get("self")
                if self_obj:
                    context.update({f"self.{k}": v for k, v in vars(self_obj).items()})

                # Пробуем форматировать строку
                try:
                    formatted_msg = message.format_map(context)
                except Exception as e:
                    formatted_msg = f"{message}  [format_error: {e}]"

                # Логируем и добавляем шаг в allure
                logging.log(level.code, formatted_msg)
                with allure.step(formatted_msg):
                    return func(*args, **kwargs)

            return wrapper

        class _LogWrapper:
            def __enter__(self):
                self._ctx = _context_manager()
                return self._ctx.__enter__()

            def __exit__(self, exc_type, exc_val, exc_tb):
                return self._ctx.__exit__(exc_type, exc_val, exc_tb)

            def __call__(self, func):
                return _decorator(func)

        return _LogWrapper()

    @staticmethod
    def _is_context_usage() -> bool:
        """
        Позволяет отличить использование как `with` от декоратора.
        Когда используется `with`, Python сразу вызывает __enter__/__exit__,
        и возвращаемый объект должен быть генератором.
        """
        # Никак не проверяем — возвращаем обе версии, но `with` сам подберёт нужную.
        # Оставлено для гибкости, если захочешь добавить логику.
        return False


step_log = StepLogger()
