import peewee as pw

user_db = pw.SqliteDatabase('users.db')

class UsersModel(pw.Model):
    class Meta:
        database = user_db

class User(UsersModel):
    id = pw.IntegerField(primary_key=True)

user_db.connect()
user_db.create_tables([User])