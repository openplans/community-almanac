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
from shapely.geometry.geo import asShape
from sqlalchemy.orm import exc
from webhelpers.paginate import Page as PaginationPage
import communityalmanac.lib.helpers as h
import simplejson

from communityalmanac.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AlmanacCreateForm(Schema):
    name = validators.String(not_empty=True)
    almanac_center = validators.String(not_empty=True)

class AlmanacController(BaseController):

    @dispatch_on(POST='_do_create')
    def create(self):
        redirect_to(h.url_for('home'))

    @validate(schema=AlmanacCreateForm(), form='create')
    def _do_create(self):
        name = self.form_result['name']

        # Prevent creation of duplicates
        try:
            almanac = meta.Session.query(Almanac).filter(Almanac.name==name).one()
            return redirect_to(h.url_for('page_create', almanac_slug=almanac.slug))
        except exc.NoResultFound:
            pass

        json = self.form_result['almanac_center']
        shape = simplejson.loads(json)
        # We've requested a LonLat from OpenLayers, so it gives us a point in
        # Plate Carree (4326)
        point = asShape(shape)
        point.srid = 4326
        slug = name_almanac(name)
        almanac = Almanac(name, slug)
        almanac.location = point

        meta.Session.save(almanac)
        meta.Session.commit()

        redirect_to(h.url_for('page_create', almanac_slug=slug))

    def view(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.transform(4326)
        c.lng, c.lat = loc.x, loc.y
        page_idx = request.GET.get('page', 1)
        try:
            page_idx = int(page_idx)
        except ValueError:
            page_idx = 1
        c.npages = len(c.almanac.pages)
        c.pagination = PaginationPage(c.almanac.pages, page=page_idx, items_per_page=10)
        cur_page = c.pagination.page
        next_page = c.pagination.next_page
        prev_page = c.pagination.previous_page
        per_page = c.pagination.items_per_page
        if next_page:
            start = ((next_page-1) * per_page) + 1
            end = start + per_page - 1
            end = min(end, c.npages)
            c.next_page_text = '%d - %d' % (start, end)
            c.next_page_url = '%s?page=%s' % (request.path_url, next_page)
        if prev_page:
            start = (prev_page-1) * per_page
            end = (start + per_page - 1) + 1
            start = max(start, 1)
            c.prev_page_text = '%d - %d' % (start, end)
            c.prev_page_url = '%s?page=%s' % (request.path_url, prev_page)
        c.showing_start = ((cur_page-1) * per_page) + 1
        c.showing_end = cur_page * per_page
        c.showing_end = min(c.showing_end, c.npages)
        c.pages = c.pagination.items
        return render('/almanac/view.mako')

    @jsonify
    def center(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location
        return dict(lat=loc.x, lng=loc.y)

    def pages_kml(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        return render('/page/kml.mako')
