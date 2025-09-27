# i18n/formatting.py
from __future__ import annotations

from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

try:
    from babel.dates import format_datetime as _babel_dt
    from babel.numbers import format_currency as _babel_currency

    _HAS_BABEL = True
except Exception:
    _HAS_BABEL = False

_DEF_TZ = "Europe/Warsaw"


def _quantize_money(x) -> Decimal:
    if not isinstance(x, Decimal):
        x = Decimal(str(x))
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_money(amount, currency: str = "USD", locale: str = "en") -> str:
    amt = _quantize_money(amount)
    if _HAS_BABEL:
        return _babel_currency(amt, currency, locale=locale)
    return f"{amt} {currency}"


def format_dt(dt: datetime, locale: str = "en") -> str:
    if _HAS_BABEL:
        return _babel_dt(dt, locale=locale)
    # fallback грубый, но живой
    return dt.strftime("%Y-%m-%d %H:%M")
