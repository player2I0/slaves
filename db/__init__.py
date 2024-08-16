import peewee as pw
import playhouse.fields as phf

user_db = pw.SqliteDatabase('users.db')

class UsersModel(pw.Model):
    class Meta:
        database = user_db

class User(UsersModel):
    id = pw.IntegerField(primary_key=True)
    ownerId = pw.IntegerField(default=-1)
    slaves = phf.PickleField(default=set())

    def enslave(self, owner):
        self.ownerId = owner.id
        owner.slaves.add(self.id)
        
        self.save()
        owner.save()

    def is_enslaved(self):
        return self.ownerId != -1

'''
class UserLink(UsersModel):
    user = pw.ForeignKeyField(User)
    link = pw.TextField()
'''

user_db.connect()
user_db.create_tables([User])