#    RSS2Discord
#    Copyright (C) 2017  Jacob Wiltse
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
