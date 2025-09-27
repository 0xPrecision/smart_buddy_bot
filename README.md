![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Platform](https://img.shields.io/badge/platform-Telegram-blue?logo=telegram&logoColor=white)
![Code style: Black](https://img.shields.io/badge/code%20style-black-000000?logo=python&logoColor=white)
![Imports: isort](https://img.shields.io/badge/imports-isort-ef8336?logo=python&logoColor=white)
![Linter: Ruff](https://img.shields.io/badge/linter-ruff-e07a5f?logo=ruff&logoColor=white)


# 🧠 SmartBuddy — Your AI Companion for Solana Wallet Analytics

## About the Project

**SmartBuddy** — is a Telegram bot for analyzing Solana wallets using the Helius API with AI-powered insights from large language models (LLMs, e.g. Mixtral via Hugging Face).  
The bot stores and displays your analysis history, lets you search by wallet or nickname, clear history, and guides you through a simple FSM-based dialogue.

Instead of digging through raw blockchain transactions, SmartBuddy helps both beginners and traders quickly navigate wallet activities and get high-quality, human-like analytics (AI summary) without requiring deep blockchain knowledge.  
The bot also comes with **built-in multilingual support (i18n)** — English and Russian are included out of the box.


---

## 📁 Project Structure

<details>
<summary>Expand the project tree</summary>

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

## 🗂️ Key modules and their purpose:

- **`api/helius/get_transactions.py`** — fetches wallet transactions via Helius API and builds activity summaries.  
- **`api/hugging_face/get_ai_analyze.py`** — Hugging Face API wrapper for generating AI analytics.  
- **`config_data/env.py`** — loads environment variables from `.env`.  
- **`database/common/models.py`** — Peewee models (`User`, `Analysis`).  
- **`handlers/default_handlers/`** — bot command handlers (`/start`, `/help`, `/analyze`, `/search_analysis`, `/history`, `/clear_history`, `/stop`).  
- **`handlers/default_handlers/common_handler.py`** — FSM dialogue logic (address, nickname, etc.).
- **`i18n/locales/`** — Translation files in JSON format.
  - `core.py` —  Core of the localization system: loads dictionaries, handles language selection, provides the `t()` function, and safe string formatting.
  - `i18n/formatting.py` — Helper functions for formatting dates, currencies, and numbers depending on the locale.  
  - `i18n/middleware.py` — Middleware for integrating i18n into the Telegram bot: detects the user’s language and automatically applies translations.  
- **`keyboards/inline/help_button.py`** — inline “Help” button.  
- **`states/state.py`** — FSM states (`waiting_for_address`, `pending_address`).  
- **`utils/misc/constants.py`** — constants (e.g. `TIMEOUT_SECONDS`).  
- **`utils/`** — support modules:  
  - `ai_helpers.py` — AI/LLM integration  
  - `analysis_helpers.py` — FSM step handling  
  - `bot_helpers.py` — Telegram utilities, formatting  
  - `search_helpers.py` — DB search helpers  
  - `wait_timer.py` — user timeout handling  

Other project files:  
- **`.env`** — secrets (never commit).  
- **`.gitignore`** — Git ignore rules (envs, caches, DB, IDE configs).  
- **`main.py`** — entry point: DB init + polling loop.  
- **`requirements.txt`** — dependencies. 


---

## 🚀 Quick Start

1. **Clone the repository and go to the project directory:**
    ```bash
    git clone https://github.com/st-saw/smartbuddy.git
    cd smart_buddy_bot
    ```

2. **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # or .\venv\Scripts\activate for Windows
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file and add your keys:**
    ```
    TELEGRAM_BOT_TOKEN=your_bot_token
    HELIUS_API_KEY=your_helius_key
    HUGGING_FACE_TOKEN=your_hugging_face_token
    ```

5. **Run the bot:**
    ```bash
    python main.py
    ```

    On the first launch, the database and tables will be created automatically.

---

## ⚡ Main Bot Commands

- `/start` — launch the bot and register yourself  
- `/help` — show this help message  
- `/analyze` — analyze a Solana wallet by address  
- `/search_analysis` — find previous analysis by wallet or nickname  
- `/history` — view your analysis history  
- `/clear_history` — clear your analysis history  
- `/stop` — cancel the current dialog  

---

## 🧩 How Conversations Work (FSM)

SmartBuddy uses a **step-by-step dialog** (finite state machine) to guide you:  
1. Enter a wallet address  
2. Choose a nickname  
3. Get or search analysis results  

You can break out of the flow anytime with `/stop`.

---

## 🌍 Internationalization (i18n)

- Ready-to-use **English and Russian translations** (`i18n/locales/en.json`, `ru.json`)  
- Easy to extend for any other language by adding new JSON files  
- Translation helper functions and middleware included (`core.py`, `middleware.py`, `formatting.py`)  

---

## 👨‍💻 Author & Support

Telegram: [@OxPrecision](https://t.me/OxPrecision)

---

## 🛡️ Important

- **Do not publish your secret keys!**  
- The `.env` file must be added to `.gitignore`.  
- Customize and extend the project for your needs!  

---

## 📄 License

This project is distributed under the MIT License. See [LICENSE](./LICENSE) for details.

**Good luck analyzing Solana wallets with SmartBuddy! 🚀**

---

© 2025 Nikita OxPrecision. All rights reserved.
