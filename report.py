from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from states import HomeworkStates
from keyboards import cancel_kb, homework_pages_done_kb, homework_task_done_kb, main_menu_kb

router = Router(name="homework")


@router.callback_query(F.data == "menu:homework")
async def cb_homework_start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(HomeworkStates.date)
    await call.message.edit_text(
        "📝 Формування Д/З\n\nКрок 1/6. Введіть дату (наприклад, 31.08.2026):",
        reply_markup=cancel_kb(),
    )
    await call.answer()


@router.message(HomeworkStates.date, F.text)
async def hw_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text.strip())
    await state.set_state(HomeworkStates.day)
    await message.answer("Крок 2/6. Вкажіть день (наприклад, День 5):", reply_markup=cancel_kb())


@router.message(HomeworkStates.day, F.text)
async def hw_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text.strip())
    await state.set_state(HomeworkStates.variant)
    await message.answer("Крок 3/6. Вкажіть варіант (наприклад, Варіант 2):", reply_markup=cancel_kb())


@router.message(HomeworkStates.variant, F.text)
async def hw_variant(message: Message, state: FSMContext):
    await state.update_data(variant=message.text.strip())
    await state.set_state(HomeworkStates.count)
    await message.answer("Крок 4/6. Вкажіть кількість завдань (число):", reply_markup=cancel_kb())


@router.message(HomeworkStates.count, F.text)
async def hw_count(message: Message, state: FSMContext):
    txt = message.text.strip()
    if not txt.isdigit() or int(txt) <= 0:
        await message.answer("Будь ласка, введіть додатне ціле число.", reply_markup=cancel_kb())
        return
    await state.update_data(count=int(txt), pages=[])
    await state.set_state(HomeworkStates.pages)
    await message.answer(
        "Крок 5/6. Надішліть фото сторінок домашнього завдання (можна декілька повідомлень).\n"
        "Коли завершите — натисніть кнопку нижче.",
        reply_markup=homework_pages_done_kb(),
    )


@router.message(HomeworkStates.pages, F.photo)
async def hw_pages_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    pages = data.get("pages", [])
    pages.append(message.photo[-1].file_id)
    await state.update_data(pages=pages)
    await message.answer(
        f"Додано сторінку ({len(pages)} шт.). Надішліть ще фото або натисніть «Далі».",
        reply_markup=homework_pages_done_kb(),
    )


def _header(data: dict) -> str:
    return f"Д/З {data.get('day', '')} {data.get('variant', '')}".strip()


@router.callback_query(HomeworkStates.pages, F.data == "hw:pages_done")
async def hw_pages_done(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pages = data.get("pages", [])
    if not pages:
        await call.answer("Спочатку завантажте хоча б одну сторінку.", show_alert=True)
        return

    header = f"*{_header(data)}*"
    if len(pages) == 1:
        await call.message.answer_photo(pages[0], caption=header, parse_mode="Markdown")
    else:
        media = [InputMediaPhoto(media=fid) for fid in pages]
        media[0].caption = header
        media[0].parse_mode = "Markdown"
        await call.message.answer_media_group(media)

    await state.update_data(task_index=1, task_photos=[])
    await state.set_state(HomeworkStates.task_photos)
    await call.message.answer(
        f"Крок 6/6. Завдання 1/{data['count']}.\nНадішліть фото товарів для цього завдання, "
        "потім натисніть «Готово».",
        reply_markup=homework_task_done_kb(),
    )
    await call.answer()


@router.message(HomeworkStates.task_photos, F.photo)
async def hw_task_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    task_photos = data.get("task_photos", [])
    task_photos.append(message.photo[-1].file_id)
    await state.update_data(task_photos=task_photos)
    await message.answer(
        f"Додано фото ({len(task_photos)} шт.) для завдання {data['task_index']}/{data['count']}.",
        reply_markup=homework_task_done_kb(),
    )


@router.callback_query(HomeworkStates.task_photos, F.data == "hw:task_done")
async def hw_task_done(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photos = data.get("task_photos", [])
    if not photos:
        await call.answer("Спочатку завантажте хоча б одне фото товару.", show_alert=True)
        return

    task_index = data["task_index"]
    count = data["count"]
    caption = f"*{_header(data)}*\n\n*Завдання {task_index}*"

    if len(photos) == 1:
        await call.message.answer_photo(photos[0], caption=caption, parse_mode="Markdown")
    else:
        media = [InputMediaPhoto(media=fid) for fid in photos]
        media[0].caption = caption
        media[0].parse_mode = "Markdown"
        await call.message.answer_media_group(media)

    if task_index >= count:
        await state.clear()
        await call.message.answer("✅ Д/З сформовано повністю!", reply_markup=main_menu_kb())
    else:
        await state.update_data(task_index=task_index + 1, task_photos=[])
        await call.message.answer(
            f"Завдання {task_index + 1}/{count}.\nНадішліть фото товарів для цього завдання, "
            "потім натисніть «Готово».",
            reply_markup=homework_task_done_kb(),
        )
    await call.answer()
