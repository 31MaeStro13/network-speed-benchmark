# Network Speed Benchmark CLI

Консольная утилита на Python для точного замера скорости интернет-соединения путем последовательной загрузки файла.

## Ключевые инженерные решения
- **Zero-Memory Overhead:** Потоковое чтение данных чанками по 64 КБ (`stream=True`) без накопления тела ответа в RAM.
- **Изоляция от CDN-кэша:** Заголовки `Cache-Control: no-cache` и cache-buster query-параметр для замера реальной пропускной способности канала.
- **Отказоустойчивость:** Раздельные таймауты на подключение (5с) и передачу данных (30с), перехват сетевых исключений.
- **Строгая валидация:** Проверка схемы URL, статуса ответа (`raise_for_status`) и фильтрация некорректных MIME-типов (`Content-Type`).

## Требования
- Python 3.10+
- Менеджер пакетов [uv](https://github.com/astral-sh/uv) (рекомендуется) или стандартный `pip`

## Установка и запуск

Клонируйте репозиторий:
```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd testovoe
```

### Запуск через `uv`:
```bash
uv run python main.py "https://proof.ovh.net/files/10Mb.dat"
```

### Или через стандартный `venv`:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
python main.py "https://proof.ovh.net/files/10Mb.dat"
```
