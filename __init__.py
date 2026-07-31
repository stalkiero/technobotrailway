from aiogram import Router, F
from aiogram.types import CallbackQuery

import database as db
from keyboards import confirm_clear_kb, back_to_menu_kb, main_menu_kb
from timers import cancel_timer

router = Router(name="clear")


@router.callback_query(F.data == "menu:clear")
async def cb_clear_ask(call: CallbackQuery):
    await call.message.edit_text(
        "Ви впевнені, що хочете повністю очистити журнал?",
        reply_markup=confirm_clear_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "clear:confirm")
async def cb_clear_confirm(call: CallbackQuery):
    user_id = call.from_user.id
    conn = await db.get_connection(user_id)
    try:
        await db.clear_all_exits(conn)
    finally:
        await conn.close()
    cancel_timer(user_id)

    await call.message.edit_text("🗑 Журнал очищено.", reply_markup=main_menu_kb())
    await call.answer("Журнал очищено")
