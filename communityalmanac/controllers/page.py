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

from communityalmanac.model import Comment
from communityalmanac.model import Map
from communityalmanac.model import Page
from communityalmanac.model import Story
from communityalmanac.model import meta
from formencode import Schema
from formencode import validators
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from communityalmanac.lib.base import BaseController, render
from shapely.geometry.geo import asShape
from shapely import wkb
import communityalmanac.lib.helpers as h
import simplejson

log = logging.getLogger(__name__)

class PageCommentForm(Schema):
    fullname = validators.String(not_empty=True)
    email = validators.Email(not_empty=True)
    website = validators.String()
    text = validators.String(not_empty=True)


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

        meta.Session.add(page)
        meta.Session.commit()

        h.remove_session_media_items()

        redirect_to(h.url_for('page_view', almanac=almanac, page=page))

    @dispatch_on(POST='_do_comment')
    def view(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.media_items = h.render_media_items(c.page.media)
        #c.comment_form = render('/comment/form.mako')
        return render('/page/view.mako')

    @validate(schema=PageCommentForm(), form='view')
    def _do_comment(self, almanac_slug, page_slug):
        almanac = h.get_almanac_by_slug(almanac_slug)
        page = h.get_page_by_slug(almanac, page_slug)
        comment = Comment(fullname=self.form_result['fullname'],
                          email=self.form_result['email'],
                          website=self.form_result['website'],
                          text=self.form_result['text'],
                          )
        comment.page_id = page.id
        meta.Session.add(comment)
        meta.Session.commit()
        redirect_to(h.url_for('page_view', almanac=almanac, page=page))


    @dispatch_on(POST='_do_form_text')
    @jsonify
    def form_text(self, almanac_slug):
        return dict(html=render('/media/story/form.mako'))

    @dispatch_on(POST='_do_form_map')
    @jsonify
    def form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location
        return dict(html=render('/media/map/form.mako'),
                    lat=loc.x, lng=loc.y,
                    )

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
        # Stupid asShape returns a PointAdapter instead of a Point.  We round
        # trip it through wkb to get the correct type.
        location = wkb.loads(asShape(shape).to_wkb())

        map = Map()
        map.location = location
        media_items = h.get_session_media_items()
        map.order = len(media_items)
        media_items.append(map)
        session.save()

        return render('/media/map/item.mako', extra_vars=dict(editable=True,
                                                              map=map,
                                                              id='pagemedia_%d' % (len(media_items)-1),
                                                              geometry=json,
                                                              ))
