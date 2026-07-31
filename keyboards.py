from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import EXIT_TYPES


def main_menu_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="📋 Журнал виходів", callback_data="menu:journal")
    b.button(text="📄 Звіт", callback_data="menu:report")
    b.button(text="🗑 Очистити журнал", callback_data="menu:clear")
    b.button(text="📝 Формування Д/З", callback_data="menu:homework")
    b.adjust(1)
    return b.as_markup()


def back_to_menu_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🔙 У головне меню", callback_data="menu:main")
    return b.as_markup()


def exit_types_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for key, meta in EXIT_TYPES.items():
        b.button(text=meta["title"], callback_data=f"exittype:{key}")
    b.button(text="🔙 Назад", callback_data="menu:main")
    b.adjust(1)
    return b.as_markup()


def exit_start_kb(type_key: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Вийшов", callback_data=f"exit:start:{type_key}")
    b.button(text="🔙 Назад", callback_data="menu:journal")
    b.adjust(1)
    return b.as_markup()


def exit_active_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🔙 Прийшов", callback_data="exit:return")
    b.button(text="⏳ Затримка (+5 хв)", callback_data="exit:delay")
    b.adjust(1)
    return b.as_markup()


def confirm_second_exit_kb(type_key: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Все одно вийти", callback_data=f"exit:forcestart:{type_key}")
    b.button(text="🔙 Скасувати", callback_data="menu:journal")
    b.adjust(1)
    return b.as_markup()


def confirm_clear_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Так, очистити", callback_data="clear:confirm")
    b.button(text="🔙 Скасувати", callback_data="menu:main")
    b.adjust(1)
    return b.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🔙 Скасувати", callback_data="menu:main")
    return b.as_markup()


def homework_pages_done_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Сторінки завантажено, далі", callback_data="hw:pages_done")
    b.button(text="🔙 Скасувати", callback_data="menu:main")
    b.adjust(1)
    return b.as_markup()


def homework_task_done_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Завдання готове, далі", callback_data="hw:task_done")
    b.button(text="🔙 Скасувати", callback_data="menu:main")
    b.adjust(1)
    return b.as_markup()
