import peewee

db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db
