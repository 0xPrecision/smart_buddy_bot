from telebot.types import Message

from api.helius.get_transactions import get_transactions, parse_transactions
from api.hugging_face.get_ai_analyze import mixtral_hf_analysis
from config_data.bot_instance import bot
from i18n.core import tr


def analyze_wallet_with_ai(wallet_address: str, message: Message, tr) -> str | None:
    """
    Analyzes 100 Solana wallet transactions via LLM and returns a short AI summary.

    Args:
    wallet_address (str): Solana wallet address to analyze.
    message (Message, optional): Telegram message object for error notifications.

    Returns:
    str | None: Short analytical model output for the wallet, or None in case of error.
    """
    response = get_transactions(wallet_address)
    info = parse_transactions(response)
    wallet_prompt_data = {
        "top_tokens": info["top_tokens"],
        "balance": info["balance"],
        "tx_in": info["tx_in"],
        "tx_out": info["tx_out"],
        "tx_list": info["tx_list"],
        "big_trades": info["big_trades"],
        "airdrops": info["airdrops"],
    }
    prompt = build_wallet_prompt(wallet_prompt_data)
    ai_analysis = mixtral_hf_analysis(prompt, message, tr)
    if ai_analysis is None:
        bot.send_message(
            message.chat.id,
            tr("ai_helpers.messages.ne-udalos-poluchit-ai-analiz", ctx=message),
        )
    return ai_analysis


def build_wallet_prompt(info: dict) -> str:
    """
    Builds a text prompt for LLM based on the transaction summary of a wallet.

    Args:
    info (dict): Dictionary with aggregated transaction data (top tokens, balance, incoming/outgoing, trades, drops, etc.).

    Returns:
    str: Ready-to-use text prompt for the language model.
    """
    return f"\nОтветь на русском языке.\nПроанализируй активность Solana-кошелька по данным:\n- Топ токены: {', '.join(info.get('top_tokens', []))}\n- Баланс: {info.get('balance', '?')} SOL\n- Входящие: {info.get('tx_in', '?')}, исходящие: {info.get('tx_out', '?')}\n- Последние 5 транзакций:\n{chr(10).join(info.get('tx_list', []))}\n- Крупные сделки: {info.get('big_trades', 'нет')}\n- Дропы: {info.get('airdrops', 'нет')}\nВ результате не указывай названия токенов, а делай вывод по стилю, стратегиям, рискам, активности владельца.\nОтветь как профессиональный криптоаналитик для клиента на русском языке, но без воды, только суть. Ответ должен быть не более 1000 символов.\n".strip()
