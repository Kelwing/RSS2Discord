from peewee import *
db = SqliteDatabase('feeds.db')

class BaseModel(Model):
    class Meta:
        database = db

class Feed(BaseModel):
    url = CharField(max_length=500)
    initialized = BooleanField(default=False)


class Article(BaseModel):
    id = CharField(max_length=500)
    title = CharField(max_length=300)
    link = CharField(max_length=500)
    summary = CharField(max_length=500)
    feed = ForeignKeyField(Feed)


class Destination(BaseModel):
    url = CharField(max_length=200)


# Many-to-many relationship :-)
class Link(BaseModel):
    feed = ForeignKeyField(Feed)
    webhook = ForeignKeyField(Destination)
