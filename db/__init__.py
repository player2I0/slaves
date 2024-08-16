import peewee as pw
import playhouse.fields as phf

user_db = pw.SqliteDatabase('users.db')

class UsersModel(pw.Model):
    class Meta:
        database = user_db

class User(UsersModel):
    id = pw.IntegerField(primary_key=True)
    ownerId = pw.IntegerField()
    slaves = phf.CompressedField()

user_db.connect()
user_db.create_tables([User])