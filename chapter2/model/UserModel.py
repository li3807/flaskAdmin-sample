from datetime import datetime

import peewee

from chapter2.model.BaseModel import BaseModel


class UserModel(BaseModel):
    username = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)
    remark = peewee.CharField(max_length=256, null=True)
    createTime = peewee.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username
