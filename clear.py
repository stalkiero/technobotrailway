from aiogram import Router, F
from aiogram.types import CallbackQuery

import database as db
from keyboards import back_to_menu_kb

router = Router(name="report")


@router.callback_query(F.data == "menu:report")
async def cb_report(call: CallbackQuery):
    conn = await db.get_connection(call.from_user.id)
    try:
        rows = await db.get_all_exits(conn)
    finally:
        await conn.close()

    if not rows:
        text = "Журнал порожній."
    else:
        lines = ["Журнал виходів", ""]
        for type_title, start_time, end_time, delayed in rows:
            title = type_title.split(" ", 1)[-1] if " " in type_title else type_title
            suffix = " (затримка)" if delayed else ""
            lines.append(f"• {start_time}–{end_time} — {title}{suffix}")
        text = "\n".join(lines)

    await call.message.edit_text(text, reply_markup=back_to_menu_kb())
    await call.answer()
