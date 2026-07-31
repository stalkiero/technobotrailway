from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards import main_menu_kb

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state):
    await state.clear()
    await message.answer(
        "👋 Вітаю у боті «Журнал Техно»!\nОберіть розділ:",
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(call: CallbackQuery, state):
    await state.clear()
    await call.message.edit_text("Головне меню. Оберіть розділ:", reply_markup=main_menu_kb())
    await call.answer()
