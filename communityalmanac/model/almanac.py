# Community Almanac - A place for your stories.
# Copyright (C) 2009  Douglas Mayle, Robert Marianski,
# Andy Cochran, Chris Patterson

# This file is part of Community Almanac.

# Community Almanac is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Community Almanac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Community Almanac.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import Column, Integer, ForeignKey, Unicode, Numeric, Boolean, String
from sqlalchemy.orm import relation

from meta import Base, storage_SRID
from sqlgeotypes import POINT
import meta

class Almanac(Base):
    __tablename__ = 'almanacs'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    slug = Column(String, unique=True)
    location = Column(POINT(storage_SRID))

    def __init__(self, name, slug, id=None):
        self.name = name
        self.slug = slug
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Almanac(id=%d, name=%s)>' % (self.id, self.name)

    @classmethod
    def get_by_slug(cls, slug):
        return meta.Session.query(Almanac).filter(Almanac.slug == slug).one()

    @classmethod
    def latest(cls):
        #FIXME we'll need to store created/modified times
        return meta.Session.query(Almanac).all()

class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    almanac_id = Column(Integer, ForeignKey('almanacs.id'))
    name = Column(Unicode)
    slug = Column(String)
    description = Column(Unicode)
    geo_place = Column(Unicode(200))
    geo_lat = Column(Numeric(11,8))
    geo_lng = Column(Numeric(11,8))

    pages = relation("Almanac", backref="pages")

    def __init__(self, name, slug, description=None, location=(None, None), id=None):
        self.name = name
        self.slug = slug
        if description is not None:
            self.description = description
        if location is not None:
            self.geo_lat, self.geo_lon = location
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Page(id=%d, name=%s)>' % (self.id, self.name)

    @classmethod
    def get_by_slug(cls, almanac, slug):
        query = meta.Session.query(Page)
        query = query.filter(Page.almanac_id == almanac.id)
        query = query.filter(Page.slug == slug)
        return query.one()


class Media(Base):
    __tablename__ = 'medias'

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('pages.id'))
    text = Column(Unicode)
    order = Column(Integer)
    discriminator = Column('type', String(50))

    __mapper_args__ = dict(polymorphic_on=discriminator)

class PDFFile(Media):
    __tablename__ = 'pdfs'
    __mapper_args__ = dict(polymorphic_identity='pdf')
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    path = Column(Unicode)

class SoundFile(Media):
    __tablename__ = 'sounds'
    __mapper_args__ = dict(polymorphic_identity='sound')
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    path = Column(Unicode)

class Image(Media):
    __tablename__ = 'images'
    __mapper_args__ = dict(polymorphic_identity='image')
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    flickr_id = Column(String)

class Story(Media):
    __tablename__ = 'stories'
    __mapper_args__ = dict(polymorphic_identity='story')
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)

class Map(Media):
    __tablename__ = 'maps'
    __mapper_args__ = dict(polymorphic_identity='map')
    id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    location = Column(POINT(storage_SRID))


class User(Base):

    #define name of table
    __tablename__ = "users"

    #its columns
    id =                 Column(Integer, primary_key=True)
    email_address =      Column(Unicode(100), nullable=False)
    password =           Column(Unicode(100), nullable=False)
    super_user =         Column(Boolean, nullable=False, default=False)

    pages = relation("Page", backref="user")
