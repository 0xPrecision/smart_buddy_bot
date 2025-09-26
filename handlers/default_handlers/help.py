from telebot.types import Message, CallbackQuery
from config_data.bot_instance import bot
from keyboards.inline.help_button import gen_markup


#: Текст справки для вывода пользователю, оформленный в HTML.
HELP_TEXT = (
    "🆘 <b>Справка</b> 🆘\n\n"
    "Я могу анализировать стратегии Solana-кошельков с помощью ИИ!\n\n"
    "<b>Команды:</b>\n\n"
    "<b>/start</b> — Запуск бота 🚀\n"
    "<b>/stop</b> — Если что-то пошло не так 🛑\n"
    "<b>/help</b> — Это сообщение ℹ️\n"
    "<b>/analyze</b> — Анализировать Solana-кошелёк 🔍\n"
    "<b>/search_analysis</b> — Поиск анализа по кошельку или никнейму 🔎\n"
    "<b>/history</b> — Моя история анализов 📜\n"
    "️<b>/clear_history</b> — Удаление истории анализов 🗑\n"
)


@bot.message_handler(commands=["help"])
def send_help(message: Message) -> None:
    """
    Sends the user detailed help with bot commands and features.
    
    Args:
    message (telebot.types.Message): Incoming Telegram message from the user.
	"""
    bot.send_message(
        message.chat.id,
        HELP_TEXT,
        parse_mode="HTML",
        reply_markup=gen_markup(),  # Клавиатура с inline-кнопкой "Справка".
    )


@bot.callback_query_handler(func=lambda call: call.data == "help")
def callback_help(call: CallbackQuery) -> None:
    """
    Handles the press on the "Help" inline button, sending the user a help message.
    
    Args:
    call (telebot.types.CallbackQuery): Callback query from the user (button press).
	"""
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, HELP_TEXT, parse_mode="HTML")
