from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_themes_keyboard(themes):
    themes_ikb = InlineKeyboardMarkup(row_width=2)
    for theme in themes:
        themes_ikb.insert(InlineKeyboardButton(text=theme, callback_data=theme))
    return themes_ikb


def get_tasks_keyboard(tasks):
    tasks_ikb = InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        task = list(map(str, task))
        tasks_ikb.insert(InlineKeyboardButton(text=task[2], callback_data=task[2]))
    return tasks_ikb

