from peewee import * 
import os

db = SqliteDatabase(os . path . join ( os . path . dirname ( os . path . realpath ( __file__ )), 'database.db'))


class BasicModel(Model):
    user_id = IntegerField()

    class Meta:
        database = db
        order_by = "user_id"


class User_plan(BasicModel):
    plan = CharField()

    class Meta:
        db_table = "user_plans"


class User_plan_state(BasicModel):
    add_state = IntegerField()
    del_state = IntegerField()

    class Meta:
        db_table = "user_plan_states"


class User_time_state(BasicModel):
    mon_state = IntegerField()
    tue_state = IntegerField()
    wed_state = IntegerField()
    tru_state = IntegerField()
    fri_state = IntegerField()
    sat_state = IntegerField()

    class Meta:
        db_table = 'user_time_states'
