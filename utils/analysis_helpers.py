import re

from telebot.types import Message

from config_data.bot_instance import bot
from database.common.models import Analysis, User
from handlers.default_handlers import search_analysis, stop
from i18n.core import tr
from states.state import pending_address, waiting_for_address
from utils.ai_helpers import analyze_wallet_with_ai
from utils.bot_helpers import format_result
from utils.wait_timer import cancel_timer


def process_analyze_query(message: Message, tr) -> None:
    """
    Handles the stage of requesting a Solana wallet address.

    1. Validates the address using a regular expression.
    2. Checks if this address has already been analyzed by the user.
    3. If valid, requests a nickname for this wallet.

    Args:
    message (Message): Telegram message object from the user.
    """
    user_id = message.from_user.id
    user = User.get(telegram_id=user_id)
    chat_id = message.chat.id
    query = message.text
    state = waiting_for_address.get(user_id)
    if query == "/search_analysis":
        waiting_for_address.pop(user_id, None)
    elif state == "analyze_query":
        if re.match("^[1-9A-HJ-NP-Za-km-z]{32,44}$", query):
            wallet_exists = (
                Analysis.select()
                .where((Analysis.user == user) & (Analysis.wallet_address == query))
                .exists()
            )
            if wallet_exists:
                bot.send_message(
                    chat_id,
                    tr(
                        "analysis_helpers.messages.ty-uzhe-analiziroval-etot",
                        ctx=message,
                    ),
                )
            else:
                pending_address[user_id] = query
                waiting_for_address[user_id] = "nickname_query"
                bot.send_message(
                    chat_id,
                    tr(
                        "analysis_helpers.messages.kak-hochesh-nazvat-etot", ctx=message
                    ),
                )
        else:
            bot.send_message(
                chat_id,
                tr(
                    "analysis_helpers.messages.adres-ne-sootvetstvuet-standartu",
                    ctx=message,
                ),
            )


def process_nickname(message: Message, tr) -> None:
    """
    Handles the stage of entering a nickname for a Solana wallet.

    1. Checks the nickname's uniqueness for this user.
    2. Fetches wallet transactions via the Helius API.
    3. Generates the analysis and saves it to the database.
    4. Sends the result to the user.

    Args:
    message (Message): Telegram message object from the user.
    """
    user_id = message.from_user.id
    user = User.get(telegram_id=user_id)
    chat_id = message.chat.id
    query = message.text
    state = waiting_for_address.get(user_id)
    if state == "nickname_query":
        nickname_exists = (
            Analysis.select()
            .where((Analysis.user == user) & (Analysis.nickname == query))
            .exists()
        )
        if nickname_exists:
            bot.send_message(
                chat_id,
                tr(
                    "analysis_helpers.messages.takoj-niknejm-uzhe-suschestvuet",
                    ctx=message,
                ),
            )
        else:
            wallet_analyze_info = analyze_wallet_with_ai(
                pending_address[user_id], message, tr
            )
            analysis = Analysis.create(
                user=user,
                wallet_address=pending_address[user_id],
                nickname=query,
                result=wallet_analyze_info,
            )
            bot.send_message(
                chat_id,
                format_result(analysis),
                disable_web_page_preview=True,
                parse_mode="HTML",
            )
            waiting_for_address.pop(user_id, None)
            pending_address.pop(user_id, None)
            cancel_timer(user_id)
            bot.send_message(
                chat_id,
                tr("constants.messages.mozhesh-otpravit-novuyu-komandu", ctx=message),
            )
