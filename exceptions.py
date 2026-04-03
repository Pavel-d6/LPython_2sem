

class TaskValidationError(Exception):
    """Базовое исключение для ошибок валидации задачи."""


class InvalidStatusTransitionError(TaskValidationError):
    """Недопустимый переход между статусами задачи."""


class InvalidPriorityError(TaskValidationError):
    """Приоритет задачи вне допустимого диапазона."""