# i18n/middleware.py
from __future__ import annotations

from telebot import types

# твоя Peewee-модель
# from models import User  # предполагаем, что есть user с полем locale
# если нет — просто закомментируй и юзай язык из Telegram

_SUPPORTED = {"en", "ru"}
_FALLBACK = "en"
_CONTEXT = {}  # user_id -> locale


def _normalize(lc: str | None) -> str:
    if not lc:
        return _FALLBACK
    lc = lc.lower()
    if lc.startswith("en"):
        return "en"
    if lc.startswith("ru"):
        return "ru"
    # можешь мапить uk->ru, be->ru, и т.д.
    return _FALLBACK


def get_locale_for_user(user_id: int, tg_lang: str | None) -> str:
    # 1) БД
    try:
        from database.common.models import \
            User  # локальный импорт, чтобы не ловить циклы

        u = User.get_or_none(User.telegram_id == user_id)
        if u and u.locale in _SUPPORTED:
            return u.locale
    except Exception:
        pass
    # 2) из Telegram
    return _normalize(tg_lang)


def install_locale_middleware(bot):
    @bot.middleware_handler(update_types=["message"])
    def _set_locale_msg(bot_, message: types.Message):
        user_id = message.from_user.id if message.from_user else message.chat.id
        tg_lang = getattr(message.from_user, "language_code", None)
        loc = get_locale_for_user(user_id, tg_lang)
        _CONTEXT[user_id] = loc
        setattr(message, "locale", loc)

    @bot.middleware_handler(update_types=["callback_query"])
    def _set_locale_cb(bot_, call: types.CallbackQuery):
        user_id = call.from_user.id
        tg_lang = getattr(call.from_user, "language_code", None)
        loc = get_locale_for_user(user_id, tg_lang)
        _CONTEXT[user_id] = loc
        setattr(call, "locale", loc)


def get_locale(user_id: int) -> str:
    return _CONTEXT.get(user_id, _FALLBACK)
