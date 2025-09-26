from telebot.types import Message

from utils.misc.constants import END_TEXT
from config_data.bot_instance import bot
from database.common.models import User, Analysis


@bot.message_handler(commands=["history"])
def send_history(message: Message) -> None:
    """
    Handles the /history command.
    Looks up all user analyses in the database and sends their brief history as a message.
    If the history is empty, informs the user.
    
    Args:
    message (telebot.types.Message): Incoming Telegram message from the user.
    
    Notes:
    - The date and time of each analysis are formatted as 'dd.mm.yyyy hh:mm'.
    - If the user has no analyses, a message "Request history is empty" is sent.
	"""
    user_id = message.from_user.id
    user = User.get_or_none(telegram_id=user_id)

    analyses = (
        Analysis.select()
        .where(Analysis.user == user)
        .order_by(Analysis.created_at.desc())
    )

    if analyses:
        text = "История анализов:\n\n"

        for analysis in analyses:
            text += (
                f"Дата: {analysis.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"Кошелёк: {analysis.wallet_address}\n"
                f"Никнейм: ({analysis.nickname})\n\n"
            )

        bot.send_message(message.chat.id, text)

    else:
        bot.send_message(message.chat.id, "История запросов пуста")

    bot.send_message(message.chat.id, END_TEXT)
