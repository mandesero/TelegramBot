from contextlib import ContextDecorator
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData

plan_callback = CallbackData("add", "ans")
timetable_callback = CallbackData("day", "ans")
clean_callback = CallbackData("clean", "ans")
delete_callback = CallbackData("del", "ans")