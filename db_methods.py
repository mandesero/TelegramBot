from db_models import *
from peewee import *
from decorators import *


# --- User plan methods ---

# === add plan to db ===
@database_handler(db_name = db)
def add_plan(id, plan):
    user = User_plan(
        user_id = id,
        plan = plan
    ).save()

# === del plan(number in plan list) to db ===
@database_handler(db_name = db)
def del_plan(id, number):
    user_info = User_plan.select().where(User_plan.user_id == id)
    tmp = user_info[number - 1].delete_instance()

# === clear user plan list ===
@database_handler(db_name = db)
def clear_user_plans(id):
    user_info = User_plan.delete().where(User_plan.user_id == id)
    user_info.execute()  

# === return plan list(need user_id) ===
@database_handler(db_name=db)
def return_user_plans(id):
    return User_plan.select().where(User_plan.user_id == id)

# === return the presence of a plan in the list ===
@database_handler(db_name=db)
def check_plan(id, plan):
    user_info = User_plan.select().where(
        User_plan.user_id == id and User_plan.plan == plan
        )
    return any(user_info)


# --- Users_states ---

# === create new record if user not already been ===
@database_handler(db_name=db)
def init_user_plan_state(id):
    user_states = User_plan_state.select().where(User_plan_state.user_id == id)
    if not user_states:
        user = User_plan_state(
            user_id=id,
            add_state = 0,
            del_state = 0,
        ).save()

# === add_state = True ===
@database_handler(db_name=db)
def change_add_state(id):
    query = User_plan_state.update(add_state = 1).where(User_plan_state.user_id == id)
    query.execute()

# === del_state = True ===
@database_handler(db_name=db)
def change_del_state(id):
        query = User_plan_state.update(del_state = 1).where(User_plan_state.user_id == id)
        query.execute()

# === return user plan states list ===
@database_handler(db_name=db)
def get_plan_state(id):
    state_rec = User_plan_state.get(User_plan_state.user_id == id)
    return state_rec

# === set add_state = 0 and del_state = 0 ===
@database_handler(db_name=db)
def clear_plan_states(id):
    query = User_plan_state.update(
        add_state = 0,
        del_state = 0,
    ).where(User_plan_state.user_id == id)
    query.execute()

# --- Timetable methods ---

# === create new record if user not already been ===
@database_handler(db_name=db)
def init_user_time_state(id):
    user_rec = User_time_state.select().where(User_time_state.user_id == id)
    if not user_rec:
        user = User_time_state(
            user_id = id,
            mon_state = 0,
            tue_state = 0,
            wed_state = 0,
            tru_state = 0,
            fri_state = 0,
            sat_state = 0,
    ).save()

# === set day_state = True (need "day") ===
@database_handler(db_name=db)
def set_time_state(id, day):
    if day == "monday":
        query = User_time_state.update(mon_state = 1).where(User_time_state.user_id == id)
    elif day == "tuesday":
        query = User_time_state.update(tue_state = 1).where(User_time_state.user_id == id)
    elif day == "wednesday":
        query = User_time_state.update(wed_state = 1).where(User_time_state.user_id == id)
    elif day == "trusday":
        query = User_time_state.update(tru_state = 1).where(User_time_state.user_id == id)
    elif day == "friday":
        query = User_time_state.update(fri_state = 1).where(User_time_state.user_id == id)
    elif day == "sunday":
        query = User_time_state.update(sat_state = 1).where(User_time_state.user_id == id)
    query.execute()

# === set all day states to False ===
@database_handler(db_name=db)
def clear_time_state(id):
    query = User_time_state.update(
        mon_state = 0,
        tue_state = 0,
        wed_state = 0,
        tru_state = 0,
        fri_state = 0,
        sat_state = 0
    ).where(User_time_state.user_id == id)
    query.execute()

# === return user plan states list ===
@database_handler(db_name=db)
def get_user_time_state(id):
    state_record = User_time_state.get(User_time_state.user_id == id)
    return state_record

def clear_user_states(id):
    clear_plan_states(id=id)
    clear_time_state(id=id)
