from aiogram.fsm.state import State, StatesGroup


class HomeworkStates(StatesGroup):
    date = State()          # Крок 1: дата
    day = State()            # Крок 2: день
    variant = State()        # Крок 3: варіант
    count = State()          # Крок 4: кількість завдань
    pages = State()          # Крок 5: сторінки Д/З (фото)
    task_photos = State()    # Крок 6: фото товарів для поточного завдання
