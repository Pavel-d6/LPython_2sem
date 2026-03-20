# Лабораторная работа №1. Источники задач и контракты



## Структура проекта

```
.
├── task.py                  # Модель задачи (dataclass)
├── protocol.py              # Контракт TaskSource (Protocol)
├── receiver.py              # Приёмник задач TaskReceiver
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
    ├── test_protocol.py
    ├── test_receiver.py
    ├── test_file_source.py
    └── test_generator_source.py
```



### Модель задачи

Задача (`Task`) — `dataclass` с двумя полями:

- `id` — уникальный идентификатор (непустая строка)
- `payload` — произвольные данные задачи

### Источники задач

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

Сервер запускается в Docker контейнере

```bash
cd flask_api
docker compose up --build
```

сервер доступен на `http://localhost:5000`



## Запуск тестов

```bash
pytest tests/
```

С покрытием:

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

