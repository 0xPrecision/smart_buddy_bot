import threading
from typing import Callable, Dict

timers: Dict[int, threading.Timer] = dict()


def start_waiting_timer(
    user_id: int,
    chat_id: int,
    timeout: float,
    on_timeout: Callable[[int, int], None],
) -> None:
    """
    Starts a waiting timer for the user. If a timer was already running for this user, it will be canceled.
    
    Args:
    user_id (int): Telegram user ID.
    chat_id (int): Chat ID where the dialog is taking place.
    timeout (float): Waiting time in seconds.
    on_timeout (Callable[[int, int], None]): Function called when the timer expires, with user_id and chat_id as arguments.
	"""
    if timers.get(user_id):
        timers[user_id].cancel()

    timer = threading.Timer(timeout, on_timeout, args=[user_id, chat_id])
    timers[user_id] = timer
    timer.start()


def cancel_timer(user_id: int) -> None:
    """
    Cancels the waiting timer for the user, if one was running.
    
    Args:
    user_id (int): Telegram user ID.
	"""
    if timers.get(user_id):
        timers[user_id].cancel()
        timers.pop(user_id, None)
