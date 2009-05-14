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

class TestAlmanacController(TestController):

    def test_home(self):
        response = self.app.get(url('home'), status=200)

    def test_create(self):
        response = self.app.get(url('almanac_create'), status=200)
        create_form = response.forms[0]
        create_form.set('name', u'my almanac')
        create_form.set('almanac_center', u'{"type":"Point","coordinates":[40.77194,-73.93056]}')
        response = create_form.submit()
        self.assertEqual(302, response.status_int)
        response = response.follow(status=200)
