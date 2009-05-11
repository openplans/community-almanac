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

from communityalmanac.model import Almanac
from communityalmanac.model import Page
from communityalmanac.model import meta

def test_almanac_save():
    a = Almanac(u'my first almanac', 'a1')
    meta.Session.save(a)
    meta.Session.commit()
    assert a.id, "did not save almanac to database"
    query = meta.Session.query(Almanac)
    queried = query.one()
    assert a.name == queried.name
    assert a.slug == queried.slug

def test_page_save():
    a = Almanac(u'almanac two', 'a2')
    meta.Session.save(a)
    p = Page(u'page one', 'p1')
    a.pages.append(p)
    meta.Session.save(p)
    meta.Session.commit()

    assert a.id
    assert p.id
    assert p.almanac_id == a.id
