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

from communityalmanac.tests import *
from communityalmanac.model import Almanac
from communityalmanac.model import meta

class TestPageController(TestController):

    def create_almanac(self, name, slug):
        a = Almanac(name, slug)
        meta.Session.add(a)
        meta.Session.commit()
        return a

    def test_create(self):
        almanac = self.create_almanac(u'my almanac for page', 'a4p')
        response = self.app.get(url('page_create', almanac=almanac), status=200)
