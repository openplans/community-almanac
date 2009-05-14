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

from communityalmanac.model import Map
from communityalmanac.model import Page
from communityalmanac.model import Story
from communityalmanac.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.rest import dispatch_on

from communityalmanac.lib.base import BaseController, render
from shapely.geometry import asShape
import communityalmanac.lib.helpers as h
import simplejson

log = logging.getLogger(__name__)

class PageController(BaseController):

    @dispatch_on(POST='_do_create')
    def create(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        media_items = h.get_session_media_items()
        # we render the media items here to keep the template simple
        c.media_items = h.render_media_items(media_items, editable=True)
        return render('/page/create.mako')

    def _do_create(self, almanac_slug):
        c.almanac = almanac = h.get_almanac_by_slug(almanac_slug)
        name = request.POST.get('name', u'')
        if not name:
            name = u'Unnamed'

        slug = h.name_page(almanac, name)
        page = Page(name, slug)
        almanac.pages.append(page)

        media_items = h.get_session_media_items()
        page.media.extend(media_items)

        meta.Session.save(page)
        meta.Session.commit()

        h.remove_session_media_items()

        redirect_to(h.url_for('page_view', almanac=almanac, page=page))

    def view(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.media_items = h.render_media_items(c.page.media)
        return render('/page/view.mako')

    @dispatch_on(POST='_do_form_text')
    def form_text(self, almanac_slug):
        return render('/media/story/form.mako')

    @dispatch_on(POST='_do_form_map')
    def form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location
        c.lat, c.lng = loc.x, loc.y
        return render('/media/map/form.mako')

    def _do_form_text(self, almanac_slug):
        body = request.POST.get('body', u'')
        if not body:
            abort(400)
        c.almanac = h.get_almanac_by_slug(almanac_slug)

        story = Story()
        story.text = body

        media_items = h.get_session_media_items()
        story.order = len(media_items)
        media_items.append(story)
        session.save()
        return render('/media/story/item.mako', extra_vars=dict(editable=True, story=story, id='pagemedia_%d' % (len(media_items)-1)))

    def _do_form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        json = request.POST.get('feature')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        location = asShape(shape)

        map = Map()
        map.location = location
        meta.Session.save(map)
        meta.Session.commit()

        return render('/media/map/item.mako')
