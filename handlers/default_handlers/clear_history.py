from telebot.types import Message
from config_data.bot_instance import bot
from database.common.models import User, Analysis


@bot.message_handler(commands=["clear_history"])
def clear_history(message: Message) -> None:
    """
    Handles the /clear_history command.
    Deletes all of the user's analysis records from the database and notifies the user of the result.
    
    Args:
    message (telebot.types.Message): Incoming Telegram message from the user.
	"""
    user_id = message.from_user.id
    user = User.get_or_none(telegram_id=user_id)
    if not user:
        bot.send_message(message.chat.id, "Пользователь не найден.")
        return

        # Удаляем все анализы пользователя
    deleted = Analysis.delete().where(Analysis.user == user).execute()
    if deleted > 0:
        bot.send_message(
            message.chat.id, f"История ({deleted} записей) успешно удалена."
        )
    else:
        bot.send_message(message.chat.id, "История уже пуста.")
