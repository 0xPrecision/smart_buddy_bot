from typing import Iterator

from telebot.types import Message

from config_data.bot_instance import bot
from database.common.models import Analysis, User
from states.state import waiting_for_address


def on_timeout(
    user_id: int,
    chat_id: int,
    message: Message = "Время ожидания истекло."
    "\nЧтобы начать заново, напиши команду или нажми /help.",
) -> None:
    """
    Called when the user action timeout expires.
    Clears state and sends a notification to the chat.

    Args:
    user_id (int): Telegram user ID.
    chat_id (int): Telegram chat ID.
    message (str, optional): Message to send to the user.
    """
    waiting_for_address.pop(user_id, None)
    bot.send_message(chat_id, message)


def format_result(analysis: Analysis) -> str:
    """
    Formats the analysis result for user output.

    Args:
    analysis (Analysis): Analysis object from the database.

    Returns:
    str: Ready-to-send text of the result.
    """
    short_address = shorten_address(analysis.wallet_address)
    return (
        f"Результат AI-анализа по кошельку {short_address} ({analysis.nickname}):\n\n"
        f"{analysis.result}\n\n"
        f"Дата анализа: {analysis.created_at.strftime('%d.%m.%Y %H:%M')}"
    )


def select_history(message: Message) -> Iterator[Analysis]:
    """
    Retrieves the list of user analyses by entered address or nickname.

    Args:
    message (Message): Telegram message containing the query text.

    Returns:
    Iterator[Analysis]: Iterator of user's Analysis objects,
    sorted by date.
    """
    user_id = message.from_user.id
    user = User.get(telegram_id=user_id)
    query = message.text

    analyses = (
        Analysis.select()
        .where(
            (Analysis.user == user)
            & ((Analysis.wallet_address == query) | (Analysis.nickname == query))
        )
        .order_by(Analysis.created_at.desc())
    )

    return analyses


def shorten_address(address: str, first: int = 6, last: int = 4) -> str:
    """
    Shortens a long wallet address for compact display.

    Args:
    address (str): Wallet address.
    first (int): Number of characters at the start.
    last (int): Number of characters at the end.

    Returns:
    str: Shortened address in the form "abcdef...wxyz"
    """
    if len(address) <= first + last:
        return address
    return f"{address[:first]}...{address[-last:]}"
