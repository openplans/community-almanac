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

from unittest import TestCase
from communityalmanac.model import Almanac
from communityalmanac.model import Page
from communityalmanac.model import meta

class TestModel(TestCase):
    """
    We want the database to be created from scratch before each test and dropped after
    each test (thus making them unit tests).
    """
    def setUp(self):
        meta.metadata.drop_all(meta.engine)
        meta.Session.remove()
        meta.metadata.create_all(meta.engine)

    def test_first(self):
        a = Almanac(u'my first almanac', 'first')
        meta.Session.save(a)
        meta.Session.commit()

    def test_second(self):
        self.failUnless(meta.Session.query(Almanac).first() is None)
        a = Almanac(u'my first almanac', 'first')
        p = Page(u'my first page', 'page')
        p.almanac_id = a.id
        meta.Session.save(a)
        meta.Session.save(p)
        meta.Session.commit()
