![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Platform](https://img.shields.io/badge/platform-Telegram-blue?logo=telegram&logoColor=white)
![Code style: Black](https://img.shields.io/badge/code%20style-black-000000?logo=python&logoColor=white)
![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336?logo=python&logoColor=white)
![Linter: Ruff](https://img.shields.io/badge/linter-ruff-e07a5f?logo=ruff&logoColor=white)


# 🧠 SmartBuddy — ваш ИИ-помощник для аналитики Solana-кошельков

## О проекте

**SmartBuddy** — это Telegram-бот для анализа Solana-кошельков с использованием API Helius и AI-аналитики на базе больших языковых моделей (LLM, например Mixtral через Hugging Face).  
Бот сохраняет и показывает историю ваших анализов, позволяет искать результаты по кошельку или нику, очищать историю и проводит пользователя через простой диалог на основе FSM.

Вместо того чтобы разбираться в сырых блокчейн-транзакциях, SmartBuddy помогает как новичкам, так и трейдерам быстро ориентироваться в активности кошельков и получать качественную, понятную аналитику (AI summary) без необходимости глубоко разбираться в блокчейне.  
У бота также есть **встроенная поддержка нескольких языков (i18n)** — английский и русский доступны сразу.


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
├── i18n/
│   ├── locales/
│   │   ├── en.json
│   │   └── ru.json
│   ├── __init__.py
│   ├── core.py
│   ├── formatting.py
│   └── middleware.py
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

## 🗂️ Ключевые модули и их назначение:

- **`api/helius/get_transactions.py`** — получает транзакции кошелька через API Helius и формирует сводку активности.  
- **`api/hugging_face/get_ai_analyze.py`** — обёртка над API Hugging Face для генерации AI-аналитики.  
- **`config_data/env.py`** — загружает переменные окружения из `.env`.  
- **`database/common/models.py`** — модели Peewee (`User`, `Analysis`).  
- **`handlers/default_handlers/`** — обработчики команд бота (`/start`, `/help`, `/analyze`, `/search_analysis`, `/history`, `/clear_history`, `/stop`).  
- **`handlers/default_handlers/common_handler.py`** — логика FSM-диалога (адрес, ник и т.д.).
- **`i18n/locales/`** — файлы переводов в формате JSON.
  - `core.py` —  ядро системы локализации: загружает словари, управляет выбором языка, предоставляет функцию `t()` и безопасное форматирование строк.
  - `i18n/formatting.py` — вспомогательные функции для форматирования дат, валют и чисел в зависимости от локали.  
  - `i18n/middleware.py` — middleware для интеграции i18n в Telegram-бота: определяет язык пользователя и автоматически применяет переводы.  
- **`keyboards/inline/help_button.py`** — инлайн-кнопка «Help».  
- **`states/state.py`** — состояния FSM (`waiting_for_address`, `pending_address`).  
- **`utils/misc/constants.py`** — константы (например, `TIMEOUT_SECONDS`).  
- **`utils/`** — вспомогательные модули:  
  - `ai_helpers.py` — интеграция AI/LLM  
  - `analysis_helpers.py` — обработка шагов FSM  
  - `bot_helpers.py` — Telegram-утилиты, форматирование  
  - `search_helpers.py` — вспомогательные функции поиска по БД  
  - `wait_timer.py` — обработка таймаутов пользователя  

Другие файлы проекта:  
- **`.env`** — секреты (никогда не коммитьте).  
- **`.gitignore`** — правила игнорирования Git (окружения, кэш, БД, конфиги IDE).  
- **`main.py`** — точка входа: инициализация БД + цикл polling.  
- **`requirements.txt`** — зависимости. 


---

## 🚀 Быстрый старт

1. **Клонируйте репозиторий и перейдите в директорию проекта:**
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

4. **Создайте файл `.env` и добавьте свои ключи:**
    ```
    TELEGRAM_BOT_TOKEN=your_bot_token
    HELIUS_API_KEY=your_helius_key
    HUGGING_FACE_TOKEN=your_hugging_face_token
    ```

5. **Запустите бота:**
    ```bash
    python main.py
    ```

    При первом запуске база данных и таблицы будут созданы автоматически.

---

## ⚡ Основные команды бота

- `/start` — запустить бота и зарегистрироваться  
- `/help` — показать это справочное сообщение  
- `/analyze` — проанализировать Solana-кошелёк по адресу  
- `/search_analysis` — найти предыдущий анализ по кошельку или нику  
- `/history` — посмотреть историю анализов  
- `/clear_history` — очистить историю анализов  
- `/stop` — отменить текущий диалог  

---

## 🧩 Как работает диалог (FSM)

SmartBuddy использует **пошаговый диалог** (finite state machine), чтобы вести пользователя по процессу:  
1. Введите адрес кошелька  
2. Выберите ник  
3. Получите результаты анализа  

Вы можете выйти из сценария в любой момент с помощью `/stop`.

---

## 🌍 Интернационализация (i18n)

- Готовые **английский и русский переводы** (`i18n/locales/en.json`, `ru.json`)  
- Лёгкое расширение под любой другой язык через добавление новых JSON-файлов  
- В комплекте есть вспомогательные функции перевода и middleware (`core.py`, `middleware.py`, `formatting.py`)  

---

## 👨‍💻 Автор и поддержка

Telegram: [@OxPrecision](https://t.me/OxPrecision)

---

## 🛡️ Важно

- **Не публикуйте свои секретные ключи!**  
- Файл `.env` должен быть добавлен в `.gitignore`.  
- Настраивайте и расширяйте проект под свои задачи!  

---

## 📄 Лицензия

Этот проект распространяется по лицензии MIT. Подробнее смотрите в файле [LICENSE](./LICENSE).

**Удачи в анализе Solana-кошельков с SmartBuddy! 🚀**

---

© 2025 Nikita OxPrecision. Все права защищены.
