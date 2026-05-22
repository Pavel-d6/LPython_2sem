# Лабораторная работа №4
## Структура проекта

```
.
├── task.py                  # Модель задачи (дескрипторы, статус-машина)
├── descriptors.py           # Дескрипторы ValidatedString, ValidatedPriority
├── exceptions.py            # Исключения TaskValidationError, InvalidStatusTransitionError
├── protocol.py              # Контракты TaskSource и TaskHandler (Protocol)
├── receiver.py              # Приёмник задач TaskReceiver
├── executor.py              # Асинхронный исполнитель TaskExecutor
├── Task_queue.py            # Синхронная очередь задач TaskQueue
├── conftest.py              # Конфигурация pytest
├── main.py                  # Демонстрация источников задач (синхронная)
├── main_async.py            # Демонстрация асинхронной обработки
├── handlers/
│   ├── registry.py          # Реестр обработчиков HandlerRegistry
│   └── default.py           # Обработчик по умолчанию DefaultHandler
├── src/
│   ├── sourse_from_file.py  # Источник задач из JSON-файла
│   ├── generator_source.py  # Программный генератор задач
│   └── flask_source.py      # Источник задач через HTTP (Flask API)
├── flask_api/
│   ├── app.py               # Flask-сервер
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
└── tests/
    ├── test_task.py
    ├── test_task_queue.py
    ├── test_protocol.py
    ├── test_receiver.py
    ├── test_file_source.py
    ├── test_generator_source.py
    └── test_executor.py     # Тесты асинхронного исполнителя
```

## Модель задачи

`Task` содержит поля:

- `id` — уникальный идентификатор (непустая строка, только для чтения)
- `description` — описание (валидируется дескриптором `ValidatedString`)
- `priority` — приоритет от 1 до 10 (валидируется дескриптором `ValidatedPriority`)
- `payload` — произвольные данные задачи (только для чтения)
- `task_type` — тип обработчика, по умолчанию `"default"`

Статус-машина: `PENDING → IN_PROGRESS → DONE` через методы `start()` и `complete()`.

## Контракты (Protocol)

`TaskSource` — синхронный источник задач, требует метод `get_tasks() -> list[Task]`.

`TaskHandler` — асинхронный обработчик задач, требует метод `async handle(task: Task) -> None`.

Оба контракта поддерживают runtime-проверку (`@runtime_checkable`) через `validate_source()` и `validate_handler()`.

## Источники задач

`FileTaskSource` — загружает задачи из JSON-файла. Ожидает массив объектов с полями `id`, `description`, `priority`, `payload`.

`GeneratorTaskSource` — генерирует задачи программно. Принимает количество задач и опциональную фабричную функцию `factory(index) -> Task`.

`FlaskApiTaskSource` — получает задачи от Flask-сервера по HTTP. Выполняет `GET /tasks` и парсит JSON-ответ.

`TaskReceiver` — агрегирует несколько источников. Проверяет каждый источник на соответствие контракту `TaskSource` при регистрации.

## Асинхронный исполнитель

`TaskExecutor` обрабатывает задачи из `asyncio.Queue` пулом воркеров:

- обработчик выбирается по `task.task_type` через `HandlerRegistry`
- ошибка в одном обработчике не останавливает остальные воркеры
- поддерживает контекстный менеджер (`async with`) и ручное управление (`start` / `stop`)

`HandlerRegistry` проверяет каждый обработчик на соответствие контракту `TaskHandler` при регистрации.

```python
registry = HandlerRegistry()
registry.register("default", DefaultHandler())

queue: asyncio.Queue = asyncio.Queue()
async with TaskExecutor(queue, registry, workers=3):
    pass
```

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov pytest-asyncio
```

## Запуск Flask-сервера

Сервер запускается в Docker-контейнере и доступен на `http://localhost:5001`.

```bash
cd flask_api
docker compose up --build
```

## Запуск

Синхронная демонстрация источников:

```bash
python main.py
```

Асинхронная обработка задач:

```bash
python main_async.py
```

## Запуск тестов

```bash
pytest tests/
```

С покрытием:

```bash
pytest tests/ --cov=. --cov-report=term-missing
```
