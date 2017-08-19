from peewee import *
db = SqliteDatabase('feeds.db')


class Feed(Model):
    url = CharField(max_length=500)
    initialized = BooleanField(default=False)


class Article(Model):
    id = CharField(max_length=500)
    title = CharField(max_length=300)
    link = CharField(max_length=500)
    summary = CharField(max_length=500)
    feed = ForeignKeyField(Feed)


class Destination(Model):
    url = CharField(max_length=200)


# Many-to-many relationship :-)
class Link(Model):
    feed = ForeignKeyField(Feed)
    webhook = ForeignKeyField(Destination)
