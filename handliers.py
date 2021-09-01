from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData
from main import bot, dp
from callback_datas import plan_callback, timetable_callback, clean_callback, delete_callback
from aiogram.types import Message, CallbackQuery, chat, message
from aiogram.dispatcher.filters import Command
from config import ADMIN_ID
from keyboards import choice_plans, choice_timetable, mainMenu, otherMenu, choice_clean, choice_add, choice_del_tt

import datetime
import asyncio

from parser import return_timetable
from database import *
from emodji import *
from other_methods import *

async def send_to_admin(dp):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')


@dp.message_handler(Command("start"))
async def start_bot(message: Message):

    init_user_plan_state(id=int(message.from_user.id))
    init_user_time_state(id=message.from_user.id)

    await message.answer(
        text="Бот работает в тестовом режиме.\nЕсли какая-то кнопка не работает, вызовите меню ещё раз.\n\n Нашёл баг : feedback ==> @mandesero "
    )
    await message.answer(
        text="Привет, {0.first_name}!".format(message.from_user) + hellohand,
        reply_markup=mainMenu
    )

    
@dp.message_handler(Command("update"))
async def update_timetable(message: Message):
    while True:
        main_parse()
        now = datetime.datetime.now()
        await message.answer(text='Расписание актуально на: ' + now.strftime("%d-%m-%Y %H:%M"))
        await asyncio.sleep(10000)
    

@dp.message_handler()
async def choose_action(message: Message):
    if message.text == "ПЛАНЫ" + success:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message.answer(
            text="Меню планов:",
            reply_markup=choice_plans
        )

    elif message.text == "РАСПИСАНИЕ" + success:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message.answer(
            text="Расписание:\nТолько второй курс МГУ!\n(201-220)",
            reply_markup=choice_timetable
        )

    else:
        user_id = int(message.from_user.id)
        plan_state_info = get_plan_state(id=user_id)

        if plan_state_info.add_state == 1:
            if not check_plan(id=user_id, plan=message.text):
                add_plan(
                    id=user_id,
                    plan=message.text
                )
                await message.answer("Успешно добавлен " + success)
            else:
                await message.answer("Такой план уже добавлен. " + pensive, reply_markup=choice_plans)

        elif plan_state_info.del_state == 1:
            try:
                del_plan(
                    id=user_id,
                    number=int(message.text)
                )
                await message.answer("Успешно удалён " + success)
            except:
                await message.answer("Такого плана нет в списке. " + pensive, reply_markup=choice_plans)

        else:
            try:
                day_states = get_user_time_state(id=message.from_user.id)
                time_dict = return_timetable(group=int(message.text))
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
                
                if day_states.mon_state == 1:
                    await message.answer(
                        text=convert_to_str(time_dict[1]),
                        reply_markup=choice_del_tt
                        )

                elif day_states.tue_state == 1:
                    await message.answer(
                        text=convert_to_str(time_dict[2]),
                        reply_markup=choice_del_tt
                        )

                elif day_states.wed_state == 1:
                    await message.answer(
                        text=convert_to_str(time_dict[3]),
                        reply_markup=choice_del_tt
                        )

                elif day_states.tru_state == 1:
                    await message.answer(
                        text=convert_to_str(time_dict[4]),
                        reply_markup=choice_del_tt
                        )

                elif day_states.fri_state == 1:
                    await message.answer(
                        text=convert_to_str(time_dict[5]),
                        reply_markup=choice_del_tt
                        )

                elif day_states.sat_state == 1:
                    await message.answer(
                        text=convert_to_str(time_dict[6]),
                        reply_markup=choice_del_tt
                        )
            except:
                await message.answer(text="Неизвестная команда " + pensive)

        clear_user_states(id=message.from_user.id)
        await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=message.message_id - 2
                    )
        await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=message.message_id - 1
                    )

        

# --- plan_callback ---

@dp.callback_query_handler(plan_callback.filter(ans='add'))
async def add_plan_button(call: CallbackQuery):
    await call.answer(cache_time=30)
    
    clear_user_states(id=call.from_user.id)

    change_add_state(
        id=call.from_user.id
    )

    await call.message.answer(text="Введите план ниже: " + pensil)



@dp.callback_query_handler(plan_callback.filter(ans='del'))
async def del_plan_button(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)

    clear_user_states(id=call.from_user.id)

    change_del_state(
        id=call.from_user.id
    )

    await call.message.answer(
        text="Введите план, который хотите удалить: " + pensil + '\n(Только его порядковый номер в списке всех планов)')

@dp.callback_query_handler(plan_callback.filter(ans='watch'))
async def watch_plan_button(call: CallbackQuery):
    await call.answer(cache_time=30)

    plans = return_user_plans(id=call.from_user.id)
    if plans:
        await call.message.answer(text="Ваши планы: " + listplans)
        number = 1
        for plan in plans:
            await call.message.answer(text=str(number) + ")" + tab + plan.plan)
            number += 1
    else:
        await call.message.answer(
            text="У вас ничего не запланирвано. " + pensive + "\nХотите добавить новый план?",
            reply_markup=choice_add)

@dp.callback_query_handler(plan_callback.filter(ans='clear'))
async def clear_plan_button(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    await call.message.answer(text="Вы уверены?", reply_markup=choice_clean)

@dp.callback_query_handler(plan_callback.filter(ans='cancel'))
async def clear_cancel_button(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    await call.message.answer(text="Меню планов: ", reply_markup=choice_plans)

# --- timetable callback ---

@dp.callback_query_handler(timetable_callback.filter(ans="monday"))
async def get_time_monday(call: CallbackQuery):
    await call.answer()

    clear_user_states(id=call.from_user.id)

    set_time_state(
        id=call.from_user.id,
        day="monday"
    )
    await call.message.answer(text='Номер группы?')

@dp.callback_query_handler(timetable_callback.filter(ans="tuesday"))
async def get_time_tuesday(call: CallbackQuery):
    await call.answer()

    clear_user_states(id=call.from_user.id)

    set_time_state(
        id=call.from_user.id,
        day="tuesday"
    )
    await call.message.answer(text='Номер группы?')

@dp.callback_query_handler(timetable_callback.filter(ans="wednesday"))
async def get_time_wednesday(call: CallbackQuery):
    await call.answer()

    clear_user_states(id=call.from_user.id)

    set_time_state(
        id=call.from_user.id,
        day="wednesday"
    )
    await call.message.answer(text='Номер группы?')

@dp.callback_query_handler(timetable_callback.filter(ans="trusday"))
async def get_time_trusday(call: CallbackQuery):
    await call.answer()

    clear_user_states(id=call.from_user.id)

    set_time_state(
        id=call.from_user.id,
        day="trusday"
    )
    await call.message.answer(text='Номер группы?')

@dp.callback_query_handler(timetable_callback.filter(ans="friday"))
async def get_time_friday(call: CallbackQuery):
    await call.answer()

    clear_user_states(id=call.from_user.id)

    set_time_state(
        id=call.from_user.id,
        day="friday"
    )
    await call.message.answer(text='Номер группы?')

@dp.callback_query_handler(timetable_callback.filter(ans="sunday"))
async def get_time_sunday(call: CallbackQuery):
    await call.answer()

    clear_user_states(id=call.from_user.id)

    set_time_state(
        id=call.from_user.id,
        day="sunday"
    )
    await call.message.answer(text='Номер группы?')


# --- clean_callback ---

@dp.callback_query_handler(clean_callback.filter(ans="yes"))
async def clean_all(call: CallbackQuery):
    await call.answer(cache_time=30)
    clear_user_plans(id=call.from_user.id)
    await call.message.answer(text="Очищено " + clean)

@dp.callback_query_handler(clean_callback.filter(ans="cancel"))
async def clean_all(call: CallbackQuery):
    await call.answer(cache_time=30)
    await call.message.answer(
        text="Меню планов:",
        reply_markup=choice_plans)

@dp.callback_query_handler(delete_callback.filter(ans="del"))
async def clear_tt(call: CallbackQuery):
    await call.answer(cache_time=30)
    await bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
