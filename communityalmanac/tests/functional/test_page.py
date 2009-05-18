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
from communityalmanac.model import Page
from communityalmanac.model import meta

class TestPageController(TestController):

    def create_almanac(self, name, slug):
        a = Almanac(name, slug)
        meta.Session.add(a)
        meta.Session.commit()
        return a

    def create_page(self, almanac, name, slug):
        p = Page(name, slug)
        almanac.pages.append(p)
        meta.Session.add(p)
        meta.Session.commit()
        return p

    def test_create(self):
        almanac = self.create_almanac(u'my almanac for page', 'a4p')
        response = self.app.get(url('page_create', almanac=almanac), status=200)

    def test_comment_create(self):
        a = self.create_almanac(u'test almanac for testing comment create', 'a4cc')
        p = self.create_page(a, u'test almanac for testing comment create', 'p4cc')
        response = self.app.get(url('page_view', almanac=a, page=p), status=200)
        form = response.forms['comment-form']
        form.set('fullname', u'johnny blaze')
        form.set('email', u'johnyblaze@example.com')
        form.set('website', u'http://example.com/')
        form.set('text', u'this is the actual comment')
        response = form.submit()
        self.assertEqual(302, response.status_int)
        response = response.follow(status=200)
        response.mustcontain('1 comment')
        response.mustcontain(u'johnny blaze')
