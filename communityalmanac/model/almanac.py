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

from sqlalchemy import Column, Integer, ForeignKey, Unicode, Numeric, Boolean
from sqlalchemy.orm import relation

from meta import Base

class Almanac(Base):
    __tablename__ = 'almanacs'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    def __init__(self, name, id=None):
        self.name = name
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Almanac(id=%d, name=%s)>' % (self.id, self.name)

class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    almanac_id = Column(Integer, ForeignKey('almanacs.id'))
    name = Column(Unicode)
    description = Column(Unicode)
    geo_place = Column(Unicode(200))
    geo_lat = Column(Numeric(11,8))
    geo_lng = Column(Numeric(11,8))

    def __init__(self, name, description=None, location=(None, None), id=None):
        self.name = name
        if description is not None:
            self.description = description
        if location is not None:
            self.geo_lat, self.geo_lon = location
        if id is not None:
            self.id = id

    def __repr__(self):
        return '<Page(id=%d, name=%s)>' % (self.id, self.name)

class User(Base):

    #define name of table
    __tablename__ = "users"

    #its columns
    id =                 Column(Integer, primary_key=True)
    email_address =      Column(Unicode(100), nullable=False)
    password =           Column(Unicode(100), nullable=False)
    super_user =         Column(Boolean, nullable=False, default=False)

    pages = relation("Page", backref="user")
