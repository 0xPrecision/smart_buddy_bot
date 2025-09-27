import logging

from config_data.bot_instance import bot
from database.common.models import Analysis, User, db
from handlers.default_handlers import (analyze, clear_history, common_handler,
                                       help, history, search_analysis, start,
                                       stop, unknown_command)
from i18n.core import load_locales
from i18n.middleware import install_locale_middleware
from utils.wait_timer import cancel_timer, start_waiting_timer


def main() -> None:
    """
    Entry point of the application. Starts polling for processing messages.
    """
    # Автоматически создаём таблицы, если их нет
    with db:
        db.create_tables([User, Analysis], safe=True)

    load_locales("i18n/locales")
    install_locale_middleware(bot)
    logging.basicConfig(level=logging.INFO)
    print("Bot started")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
