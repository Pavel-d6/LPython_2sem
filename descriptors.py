
from typing import Any
from exceptions import TaskValidationError, InvalidPriorityError


class ValidatedString:
    """
    Data-дескриптор для строковых атрибутов.

    Проверяет что значение является непустой строкой.
    Реализует __get__ и __set__ 
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name
        self._private = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> str:
        if obj is None:
            return self  # type: ignore[return-value]
        return getattr(obj, self._private)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"'{self._name}' должен быть строкой, получено: {type(value).__name__}"
            )
        if not value.strip():
            raise TaskValidationError(f"'{self._name}' не может быть пустым")
        setattr(obj, self._private, value)


class ValidatedPriority:
    """
    Data-дескриптор для приоритета задачи.

    Проверяет что значение является целым числом в диапазоне [1, 10].
    """

    MIN = 1
    MAX = 10

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name
        self._private = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> int:
        if obj is None:
            return self  
        return getattr(obj, self._private)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"'{self._name}' должен быть целым числом, получено: {type(value).__name__}"
            )
        if not (self.MIN <= value <= self.MAX):
            raise InvalidPriorityError(
                f"'{self._name}' должен быть в диапазоне [{self.MIN}, {self.MAX}], получено: {value}"
            )
        setattr(obj, self._private, value)