import peewee as pw
import playhouse.fields as phf

user_db = pw.SqliteDatabase('users.db')

class UsersModel(pw.Model):
    class Meta:
        database = user_db

class CottonFarm(UsersModel):
    id = pw.IntegerField(primary_key=True)
    owner = pw.ForeignKeyField()

class User(UsersModel):
    id = pw.IntegerField(primary_key=True)
    ownerId = pw.IntegerField(default=-1)
    slaves = phf.PickleField(default=[])
    name = pw.TextField()
    money = pw.FloatField(default=0)
    lang = pw.TextField(default="en")

    def enslave(self, owner):
        self.ownerId = owner.id
        
        if self.id not in owner.slaves:
            owner.slaves.append(self.id)
        
        self.save()
        owner.save()

    def is_enslaved(self):
        return self.ownerId != -1
    
    def get_owner(self):
        return User.get(User.id == self.ownerId)

'''
class UserLink(UsersModel):
    user = pw.ForeignKeyField(User)
    link = pw.TextField()
'''

user_db.connect()
user_db.create_tables([User])