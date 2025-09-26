from api.helius.get_transactions import get_transactions, parse_transactions
from api.hugging_face.get_ai_analyze import mixtral_hf_analysis
from config_data.bot_instance import bot
from telebot.types import Message


def analyze_wallet_with_ai(wallet_address: str, message: Message = None) -> str | None:
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
    ai_analysis = mixtral_hf_analysis(prompt)

    if ai_analysis is None:
        bot.send_message(
            message.chat.id, "Не удалось получить AI-анализ, попробуй позже."
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
    return f"""
Ответь на русском языке.
Проанализируй активность Solana-кошелька по данным:
- Топ токены: {', '.join(info.get('top_tokens', []))}
- Баланс: {info.get('balance', '?')} SOL
- Входящие: {info.get('tx_in', '?')}, исходящие: {info.get('tx_out', '?')}
- Последние 5 транзакций:
{chr(10).join(info.get('tx_list', []))}
- Крупные сделки: {info.get('big_trades', 'нет')}
- Дропы: {info.get('airdrops', 'нет')}
В результате не указывай названия токенов, а делай вывод по стилю, стратегиям, рискам, активности владельца.
Ответь как профессиональный криптоаналитик для клиента на русском языке, но без воды, только суть. Ответ должен быть не более 1000 символов.
""".strip()
