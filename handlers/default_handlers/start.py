from telebot.types import Message
from database.common.models import User
from config_data.bot_instance import bot
from keyboards.inline.help_button import gen_markup


@bot.message_handler(commands=["start"])
def send_welcome(message: Message) -> None:
    """
    Handles the /start command.
    Registers the user in the database (if not already present) and sends a welcome message with an inline button.
    
    Args:
    message (telebot.types.Message): Telegram message from the user.
    
    Notes:
    - User.get_or_create() ensures the user is added only once.
    - After /start the user immediately sees a button to go to help.
	"""
    telegram_id = message.from_user.id
    user, created = User.get_or_create(telegram_id=telegram_id)

    bot.send_message(
        telegram_id,
        "Привет 👋 Я бот для анализа Solana Smart-кошельков. Нажми кнопку ниже, чтобы начать и получить справку.",
        reply_markup=gen_markup(),
    )
