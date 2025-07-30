# 🧠 SmartBuddy — твой AI-напарник в мире Solana

## О проекте

**SmartBuddy** — это Telegram-бот для анализа Solana-кошельков на базе Helius API с поддержкой AI-аналитики через LLM (Mixtral 8x7B-Instruct via Hugging Face).
Бот сохраняет и показывает историю анализов, позволяет искать по кошельку или никнейму, очищать историю, поддерживает удобный FSM-диалог.

SmartBuddy помогает новичкам и трейдерам быстро ориентироваться в активностях кошельков, получать качественную “человеческую” аналитику (AI-summary), не требуя глубоких знаний блокчейна.

---

## 📁 Структура проекта

<details>
<summary>Развернуть дерево проекта</summary>

```
📦 smart_buddy_bot/
├── api/
│   ├── helius/
│   │   ├── __init__.py
│   │   └── get_transactions.py
│   └── hugging_face/
│       ├── __init__.py
│       └── get_ai_analyze.py
├── config_data/
│   ├── __init__.py
│   ├── bot_instance.py
│   └── env.py
├── database/
│   └── common/
│       ├── __init__.py
│       └── models.py
├── handlers/
│   └── default_handlers/
│       ├── __init__.py
│       ├── analyze.py
│       ├── clear_history.py
│       ├── common_handler.py
│       ├── help.py
│       ├── history.py
│       ├── search_analysis.py
│       ├── start.py
│       └── stop.py
├── keyboards/
│   └── inline/
│       ├── __init__.py
│       └── help_button.py
├── states/
│   ├── __init__.py
│   └── state.py
├── utils/
│   └── misc/
│       ├── __init__.py
│       ├── ai_helpers.py
│       ├── analysis_helpers.py
│       ├── bot_helpers.py
│       ├── constants.py
│       ├── search_helpers.py
│       └── wait_timer.py
├── .env
├── .gitignore
├── LICENSE
├── main.py
├── readme.md
└── requirements.txt
```
</details>

---

## 🗂️ Описание основных файлов

- `api/helius/get_transactions.py`  
  🔹 Функции для получения истории транзакций через REST API Helius и построения summary по активности.  


- `api/hugging_face/get_ai_analyze.py`  
  🔹 Обёртка над Hugging Face API для генерации краткой AI-аналитики по кошельку.


- `config_data/env.py`  
  🔹 Загрузка переменных окружения (`TELEGRAM_BOT_TOKEN`, `HELIUS_API_KEY`, `HUGGING_FACE_TOKEN`) из `.env`


- `database/common/models.py`  
  🔹 Peewee-модели:
  - `User` — Telegram-пользователь  
  - `Analysis` — анализ кошелька (адрес, никнейм, результат, дата)


- `handlers/default_handlers/`  
  🔹 Обработчики команд Telegram-бота:  
  `/start`, `/help`, `/analyze`, `/search_analysis`, `/history`, `/clear_history`, `/stop`


- `handlers/default_handlers/common_handler.py`  
  🔹 FSM-логика диалогов (ожидание адреса, никнейма и др.)


- `keyboards/inline/help_button.py`  
  🔹 Кнопка для вызова справки


- `states/state.py`  
  🔹 Словарь состояний:  
  `waiting_for_address`, `pending_address`


- `utils/misc/constants.py`  
  🔹 Константы:
  - `TIMEOUT_SECONDS = 600` — ожидание пользователя (сек)  
  - `END_TEXT = "Можешь отправить новую команду или /help."` — сообщение по завершении анализа


- `utils/`  
  🔹 Вспомогательные модули проекта:
  - `ai_helpers.py` — интеграция с AI/LLM-аналитикой (генерация prompt, отправка в LLM, парсинг ответа)

  - `analysis_helpers.py` — логика обработки пользовательских шагов в FSM

  - `bot_helpers.py` — базовые Telegram-утилиты и форматирование сообщений

  - `search_helpers.py` — функция для поиска анализа по базе

  - `wait_timer.py` — логика тайм-аута пользователя во время анализа  

  🔹 Все эти модули обеспечивают работу бота “под капотом” и не требуют ручной настройки


- `.env`  
  🔒 Секретные ключи (**не загружай в публичные репозитории**)


- `.gitignore`  
  🧾 Исключения для Git:

  - `.venv/`, `venv/` — виртуальное окружение Python (не хранить в репозитории)

  - `.idea/` — служебные настройки PyCharm/IntelliJ IDEA

  - `__pycache__/`, `*.pyc` — скомпилированные файлы Python и кэш-интерпретатора

  - `*.db` — база данных проекта (например, Peewee, SQLite и др.)

  - `.env` — все конфиденциальные ключи и токены

  - `.DS_Store` — системные файлы macOS (Finder)


- `main.py`  
  🔹 Точка входа. Создаёт БД и таблицы, запускает polling


- `requirements.txt`  
  📦 Список зависимостей проекта


---

## 🚀 Быстрый старт

1. **Склонируйте репозиторий и перейдите в директорию проекта:**
    ```bash
    git clone https://github.com/st-saw/smartbuddy.git
    cd smart_buddy_bot
    ```

2. **Создайте виртуальное окружение (рекомендуется):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # или .\venv\Scripts\activate для Windows
    ```

3. **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Создайте файл `.env` и добавьте ваши ключи:**
    ```
    TELEGRAM_BOT_TOKEN=ваш_токен_бота
    HELIUS_API_KEY=ваш_ключ_helius
    HUGGING_FACE_TOKEN=ваш_токен_hugging_face
    ```

5. **Запустите бота:**
    ```bash
    python main.py
    ```

    При первом запуске база данных и таблицы создадутся автоматически.

---

## ⚡ Основные команды бота

- `/start` — Запуск бота и регистрация пользователя
- `/help` — Справка и список команд
- `/analyze` — Анализировать Solana-кошелёк по адресу
- `/search_analysis` — Поиск анализа по кошельку или никнейму
- `/history` — Ваша история анализов
- `/clear_history` — Удаление истории анализов
- `/stop` — Прервать текущий диалог

---

## 🧩 FSM и обработка сообщений

Бот поддерживает FSM (finite state machine) — последовательное общение:
- Ожидание адреса
- Ожидание никнейма
- Поиск анализа по адресу/никнейму  
В любой момент можно прервать диалог командой `/stop`.

---

## 👨‍💻 Автор и поддержка

Telegram: [@OxPrecision](https://t.me/OxPrecision)

---

## 🛡️ Важно

- **Не публикуйте свои секретные ключи!**  
- Файл `.env` должен быть добавлен в `.gitignore`.
- Проект развивайте и кастомизируйте под свои задачи!

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. файл [LICENSE](./LICENSE).

**Удачи в анализе Solana-кошельков с SmartBuddy! 🚀**

---

© 2025 Nikita OxPrecision. All rights reserved.
