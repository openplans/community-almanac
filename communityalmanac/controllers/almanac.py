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

import logging

from communityalmanac.lib.helpers import name_almanac
from communityalmanac.model import Almanac
from communityalmanac.model import meta
from formencode import Invalid
from formencode import Schema
from formencode import validators
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
from shapely.geometry import asShape
from sqlalchemy.orm import exc
import communityalmanac.lib.helpers as h
import simplejson

from communityalmanac.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AlmanacCreateForm(Schema):
    name = validators.String(not_empty=True)
    almanac_center = validators.String(not_empty=True)

class AlmanacController(BaseController):

    def home(self):
        c.almanacs = Almanac.latest()
        c.is_homepage = True
        return render('/home.mako')

    @dispatch_on(POST='_do_create')
    def create(self):
        return render('/almanac/create.mako')

    @validate(schema=AlmanacCreateForm(), form='create')
    def _do_create(self):
        name = self.form_result['name']
        json = self.form_result['almanac_center']
        shape = simplejson.loads(json)
        point = asShape(shape)
        slug = name_almanac(name)
        almanac = Almanac(name, slug)
        almanac.location = point

        meta.Session.save(almanac)
        meta.Session.commit()

        redirect_to(h.url_for('almanac_view', almanac_slug=slug))

    def view(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location
        c.lat, c.lng = loc.x, loc.y
        return render('/almanac/view.mako')

    @jsonify
    def center(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location
        return dict(lat=loc.x, lng=loc.y)

    def kml(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        return render('/almanac/kml.mako')
