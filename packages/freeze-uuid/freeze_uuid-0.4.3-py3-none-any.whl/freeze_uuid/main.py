import uuid
import functools
from typing import Any, Callable, Union
from inspect import iscoroutinefunction

DEFAULT_VALUE = '00000000-0000-0000-0000-000000000000'

VALUES = [DEFAULT_VALUE]
COUNT = 0


class FakeUUID(uuid.UUID):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        global COUNT
        self.value = VALUES[COUNT] if COUNT < len(VALUES) else VALUES[-1]
        self.int = int(self.value.replace('-', ''), 16)  # type: ignore
        COUNT += 1

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, __value: object) -> bool:
        return str(__value) == self.value


def freeze_uuid(values: Union[str, list] = DEFAULT_VALUE) -> Callable:
    def inner(func: Callable) -> Callable:
        def value_magic() -> None:
            global VALUES
            if isinstance(values, str):
                VALUES = [values]
            else:
                VALUES = values

            global COUNT
            COUNT = 0

            for value in VALUES:
                uuid.UUID(value)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            value_magic()
            prev_uuid = uuid.UUID
            uuid.UUID = FakeUUID

            func_result = func(*args, **kwargs)

            uuid.UUID = prev_uuid
            return func_result

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> None:
            value_magic()
            prev_uuid = uuid.UUID
            uuid.UUID = FakeUUID

            func_result = await func(*args, **kwargs)

            uuid.UUID = prev_uuid
            return func_result

        if iscoroutinefunction(func):
            return async_wrapper

        return wrapper
    return inner


class freeze_uuid_manager:
    def __init__(self, values: Union[str, list[str]] = DEFAULT_VALUE) -> None:
        global VALUES
        if isinstance(values, str):
            VALUES = [values]
        else:
            VALUES = values

        for value in VALUES:
            uuid.UUID(value)

        global COUNT
        COUNT = 0

        self.prev_uuid = uuid.UUID

    def __enter__(self) -> None:
        uuid.UUID = FakeUUID

    def __exit__(self, *args: Any) -> None:
        uuid.UUID = self.prev_uuid
