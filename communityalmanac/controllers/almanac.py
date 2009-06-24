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

from communityalmanac.model import Almanac
from communityalmanac.model import Page
from communityalmanac.model import IndexLine
from communityalmanac.model import meta
from communityalmanac.model.meta import Session as s
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
from sqlalchemy.sql import func
from sqlalchemy import desc
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
        slug = Almanac.name_almanac(name)
        almanac = Almanac(name, slug)
        almanac.location = point

        meta.Session.save(almanac)
        meta.Session.commit()

        redirect_to(h.url_for('page_create', almanac_slug=slug))

    def view(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location_4326
        c.lng, c.lat = loc.x, loc.y
        page_idx = request.GET.get('page', 1)
        try:
            page_idx = int(page_idx)
        except ValueError:
            page_idx = 1
        pages_query = meta.Session.query(Page).filter(Page.almanac_id==c.almanac.id).filter(Page.published == True).order_by(Page.modified.desc())
        c.pagination = h.setup_pagination(pages_query, page_idx)
        c.pages = c.pagination.items
        c.npages = c.pagination.item_count
        return render('/almanac/view.mako')

    @dispatch_on(POST='_search')
    def search(self, almanac_slug, query):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location_4326
        c.lng, c.lat = loc.x, loc.y
        page_idx = request.GET.get('page', 1)
        try:
            page_idx = int(page_idx)
        except ValueError:
            page_idx = 1
        c.pagination = h.setup_pagination(c.almanac.search(query), page_idx)
        c.pages = c.pagination.items
        c.npages = c.pagination.item_count
        return render('/almanac/search.mako')

    def _search(self, almanac_slug, query=''):
        redirect_to(h.url_for('almanac_search', almanac_slug=almanac_slug, query=request.params.get('query','')))

    def index(self):
        c.indexlines = s.query(func.ts_stat('SELECT weighted FROM index_lines WHERE almanac_id = %d' % c.almanac.id))
    @jsonify
    def center(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location
        return dict(lat=loc.x, lng=loc.y)

    def pages_kml(self, almanac_slug, query):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        if query:
            c.pages = c.almanac.search(query).all()
        else:
            c.pages = c.almanac.pages
        return render('/page/kml.mako')
