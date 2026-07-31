"""
Реєстр активних asyncio-задач таймера, по одній на користувача.
Зберігається в пам'яті процесу (для простоти цього рішення).
"""
import asyncio
from typing import Dict

active_timers: Dict[int, asyncio.Task] = {}


def cancel_timer(user_id: int) -> None:
    task = active_timers.pop(user_id, None)
    if task and not task.done():
        task.cancel()
