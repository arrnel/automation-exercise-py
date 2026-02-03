import inspect
import logging
from contextlib import contextmanager
from functools import wraps
from typing import Callable, TypeVar, Optional, Generator

import allure

from src.model.enum.meta.log_level import LogLvl


T = TypeVar("T")


class SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return f"{{{key}}}"


class StepLogger:

    def __init__(self, default_level: int = LogLvl.INFO):
        self.default_level = default_level

    def log(
        self,
        message: str,
        log_level: Optional[LogLvl] = None,
    ) -> Callable[..., T] | Generator[None, None, None]:

        level = log_level or self.default_level

        @contextmanager
        def _context_manager():
            logging.log(level.code, message)
            with allure.step(message):
                yield

        def _decorator(func: Callable[..., T]) -> Callable[..., T]:

            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                bound_args = inspect.signature(func).bind_partial(*args, **kwargs)
                bound_args.apply_defaults()

                context = SafeDict(bound_args.arguments)

                self_obj = context.get("self")
                if self_obj is not None:
                    context.update(
                        {
                            f"self.{attr}": value
                            for attr, value in vars(self_obj).items()
                        }
                    )

                module = inspect.getmodule(func)
                if module is not None:
                    module_constants = {
                        name: value
                        for name, value in module.__dict__.items()
                        if name.isupper() and not callable(value)
                    }
                    context.update(module_constants)

                try:
                    formatted_message = message.format_map(context)
                except Exception as exc:
                    formatted_message = (
                        f"{message} [format_error: {exc.__class__.__name__}: {exc}]"
                    )

                logging.log(level.code, formatted_message)
                with allure.step(formatted_message):
                    return func(*args, **kwargs)

            return wrapper

        class _LogWrapper:
            def __enter__(self):
                self._ctx = _context_manager()
                return self._ctx.__enter__()

            def __exit__(self, exc_type, exc_val, exc_tb):
                return self._ctx.__exit__(exc_type, exc_val, exc_tb)

            def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
                return _decorator(func)

        return _LogWrapper()


step_log = StepLogger()
