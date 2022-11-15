import peewee as pw

database = pw.SqliteDatabase('todo.db')

class BaseModel(pw.Model):
    class Meta:
        database = database

class Todo(BaseModel):
    id = pw.CharField(primary_key=True, unique=True)
    owner = pw.CharField()
    value = pw.CharField()
    completed = pw.BooleanField()

database.create_tables([Todo])