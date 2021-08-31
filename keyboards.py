from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import inline_keyboard
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils import callback_data
from callback_datas import plan_callback, timetable_callback, clean_callback, delete_callback

from emodji import *

# --- Main menu ---

btnPlans = KeyboardButton("ПЛАНЫ" + success)
btnTimeTable = KeyboardButton("РАСПИСАНИЕ" + success)
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnPlans, btnTimeTable)

# --- Other menu ---

btnMain = KeyboardButton("BACK TO MAIN MENU")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMain)

# --- Add plan? ---

choice_plans = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить новый план" + add_one,
                callback_data=plan_callback.new(ans="add")
            )
        ],
        [
            InlineKeyboardButton(
                text="Удалить план" + del_one,
                callback_data="add:del"
            )
        ],
        [
            InlineKeyboardButton(
                text="Показать список планов" + planlist,
                callback_data="add:watch"
            )
        ],
        [
            InlineKeyboardButton(
                text="Очистить список" + rubbish,
                callback_data="add:clear"
            )
        ]
    ]
)

# --- Add timetable? ---

choice_timetable = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="ПОНЕДЕЛЬНИК",
                callback_data=timetable_callback.new(ans="monday")
            )
        ],
        [
            InlineKeyboardButton(
                text="ВТОРНИК",
                callback_data="day:tuesday"
            )
        ],
        [
            InlineKeyboardButton(
                text="СРЕДА",
                callback_data="day:wednesday"
            )
        ],
        [
            InlineKeyboardButton(
                text="ЧЕТВЕРГ",
                callback_data="day:trusday"
            )
        ],
        [
            InlineKeyboardButton(
                text="ПЯТНИЦА",
                callback_data="day:friday"
            )
        ],
        [
            InlineKeyboardButton(
                text="СУББОТА",
                callback_data="day:sunday"
            )
        ]
    ]
)
# --- Clear list YES/NO ---

choice_clean = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да",
                callback_data=clean_callback.new(ans="yes")
            )
        ],
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="clean:cancel"
            )
        ]
    ]
)

choice_add = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да",
                callback_data=plan_callback.new(ans="add")
            )
        ],
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="add:cancel"
            )
        ]
    ]
)

choice_del_tt = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Очистить",
                    callback_data=delete_callback.new(ans="del")
                )
            ]
        ]
)
