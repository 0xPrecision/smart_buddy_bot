# i18n/core.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from i18n.middleware import get_locale

_LOCALES: Dict[str, Dict[str, str]] = {}
_DEFAULT = "en"
_FALLBACK = "en"


def load_locales(dir_path: str = "locales") -> None:
    global _LOCALES
    _LOCALES.clear()
    for p in Path(dir_path).glob("*.json"):
        _LOCALES[p.stem] = _load_json(p)


def _load_json(path: Path) -> Dict[str, str]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        # допускаем как плоский словарь, так и вложенные файлы — сплющивать не будем, ты уже сделал плоский
        return data


def has_key(key: str, locale: str) -> bool:
    return locale in _LOCALES and key in _LOCALES[locale]


def _get(locale: str, key: str) -> str:
    # 1) нужная локаль, 2) FALLBACK, 3) ключ как текст
    val = _LOCALES.get(locale, {}).get(key)
    if val is None:
        val = _LOCALES.get(_FALLBACK, {}).get(key, key)
    return val


def safe_format(template: str, **kwargs: Any) -> str:
    # не падаем, если забыли аргумент; оставляем {placeholder} как есть
    class _Dict(dict):
        def __missing__(self, k):
            return "{" + k + "}"

    return template.format_map(_Dict(**kwargs))


def t(key: str, locale: str | None = None, **kwargs: Any) -> str:
    loc = locale or _DEFAULT
    template = _get(loc, key)
    return safe_format(template, **kwargs)


def tr(key: str, ctx=None, **kwargs) -> str:
    """
    ctx — объект message/call или user_id.
    """
    if ctx is None:
        loc = "en"
    elif hasattr(ctx, "locale"):
        loc = ctx.locale
    elif hasattr(ctx, "from_user"):
        loc = getattr(ctx.from_user, "language_code", "en")
    elif isinstance(ctx, int):
        loc = get_locale(ctx)
    else:
        loc = "en"

    return t(key, loc, **kwargs)
