from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def gen_markup() -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard with a single "Help" button.

    Returns:
    InlineKeyboardMarkup: Keyboard with one inline button for requesting help.

    Example:
    reply_markup = gen_markup()
    bot.send_message(chat_id, "Press the button below for help.", reply_markup=reply_markup)
    """
    keyboard = InlineKeyboardMarkup()
    help_button = InlineKeyboardButton(text="Справка", callback_data="help")
    keyboard.add(help_button)
    return keyboard
