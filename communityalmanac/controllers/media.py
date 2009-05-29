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

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
from communityalmanac.model import Map
from communityalmanac.model import Story
from communityalmanac.model import meta
from pylons.decorators import jsonify
from pylons.decorators.rest import dispatch_on
from shapely import wkb
from shapely.geometry.geo import asShape
import communityalmanac.lib.helpers as h
import simplejson

log = logging.getLogger(__name__)

class MediaController(BaseController):

    @dispatch_on(GET='donothing')
    def sort(self):
        id = request.params.get('id')
        index = request.params.get('index')
        if not id or not index:
            abort(400)
        try:
            index = int(index)
            id = int(id.split('_')[-1])
        except ValueError:
            abort(400)
        if not h.sort_media_items(id, index):
            abort(400)
        # The only useful return value is the HTTP response, so we return an
        # empty body.
        return ''

    def donothing(self, almanac_slug):
        abort(400)

    @dispatch_on(POST='_do_new_form_text')
    @jsonify
    def new_form_text(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        return dict(html=render('/media/story/form.mako'))

    @jsonify
    def _do_new_form_text(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        body = request.POST.get('body', u'')
        if not body:
            abort(400)

        page = c.almanac.new_page(self.ensure_user)

        c.story = story = Story()
        story.text = body
        story.page_id = page.id
        story.order = len(page.media)
        meta.Session.add(story)
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/story/item.mako'))

    @dispatch_on(POST='_do_edit_form_text')
    @jsonify
    def edit_form_text(self, media_id):
        c.story = h.get_media_by_id(media_id)
        return dict(html=render('/media/story/form.mako'))

    @jsonify
    def _do_edit_form_text(self, media_id):
        c.story = h.get_media_by_id(media_id)
        body = request.POST.get('body', u'')
        if not body:
            abort(400)

        c.story.text = body
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/story/item.mako'))

    @jsonify
    def text_view(self, media_id):
        c.editable = True
        c.story = h.get_media_by_id(media_id)
        return dict(html=render('/media/story/item.mako'))

    @jsonify
    def delete_text(self, media_id):
        story = h.get_media_by_id(media_id)
        meta.Session.delete(story)
        meta.Session.commit()

    @dispatch_on(POST='_do_new_form_map')
    @jsonify
    def new_form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        loc = c.almanac.location
        return dict(html=render('/media/map/form.mako'),
                    lat=loc.x, lng=loc.y,
                    )

    @jsonify
    def _do_new_form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        json = request.POST.get('feature')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        # Stupid asShape returns a PointAdapter instead of a Point.  We round
        # trip it through wkb to get the correct type.
        location = wkb.loads(asShape(shape).to_wkb())

        c.map = map = Map()
        map.location = location
        map.page_id = page.id
        map.order = len(page.media)
        meta.Session.add(map)
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/map/item.mako'),
                    map_id='pagemedia_%d' % map.order,
                    geometry=json,
                    )
