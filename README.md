# Лабораторная работа №3.

## Структура проекта

```
.
├── task.py                  # Модель задачи: класс Task со статусами и дескрипторами
├── Task_queue.py            # Очередь задач TaskQueue с итерацией и ленивыми фильтрами
├── protocol.py              # Контракт TaskSource (Protocol)
├── receiver.py              # Приёмник задач TaskReceiver
├── descriptors.py           # Data-дескрипторы: ValidatedString, ValidatedPriority
├── exceptions.py            # Иерархия исключений валидации задачи
├── conftest.py              # Конфигурация pytest
├── main.py                  # Точка входа
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
    └── test_generator_source.py
```

## Модель задачи (`task.py`)

Класс `Task` представляет единицу работы. Поля `description` и `priority` защищены data-дескрипторами с валидацией:

- `id` — уникальный идентификатор (непустая строка, только для чтения)
- `description` — описание задачи (непустая строка, проверяется `ValidatedString`)
- `priority` — приоритет от 1 до 10 (проверяется `ValidatedPriority`)
- `payload` — произвольные данные задачи (только для чтения)
- `status` — текущий статус (`PENDING → IN_PROGRESS → DONE`), меняется через `start()` / `complete()`
- `created_at` — время создания (только для чтения)
- `is_ready` — `True`, если статус `PENDING`

Недопустимый переход между статусами бросает `InvalidStatusTransitionError`.

## Дескрипторы (`descriptors.py`)

- `ValidatedString` — data-дескриптор для строковых полей: проверяет тип и непустоту значения
- `ValidatedPriority` — data-дескриптор для приоритета: проверяет тип и диапазон `[1, 10]`

## Исключения (`exceptions.py`)

- `TaskValidationError` — базовое исключение для ошибок валидации
- `InvalidStatusTransitionError` — недопустимый переход между статусами
- `InvalidPriorityError` — приоритет вне допустимого диапазона

## Очередь задач (`Task_queue.py`)

`TaskQueue` — коллекция задач с поддержкой ленивой обработки:

- `add(task)` — добавляет задачу в очередь
- `__iter__` — генераторная функция, позволяет повторный обход очереди
- `__len__` — количество задач в очереди
- `__contains__` — проверка вхождения задачи
- `filter_by_status(status)` — ленивый генератор задач с заданным статусом
- `filter_by_priority(min, max)` — ленивый генератор задач с приоритетом в диапазоне `[min, max]`

Фильтры реализованы через генераторы: данные не копируются в память, обработка выполняется по запросу.

## Источники задач

`FileTaskSource` — загружает задачи из JSON-файла. Ожидает массив объектов с полями `id` и `payload`.

`GeneratorTaskSource` — генерирует задачи программно. Принимает количество задач и опциональную фабричную функцию.

`FlaskApiTaskSource` — получает задачи от Flask-сервера по HTTP. Выполняет `GET /tasks` и парсит JSON-ответ.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov
```

## Запуск Flask-сервера

Сервер запускается в Docker-контейнере:

```bash
cd flask_api
docker compose up --build
```

Сервер доступен на `http://localhost:5000`.

## Запуск тестов

```bash
pytest tests/
```

С покрытием:

```bash
pytest tests/ --cov=. --cov-report=term-missing
```
