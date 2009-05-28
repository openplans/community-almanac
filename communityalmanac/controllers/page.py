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
        page = c.almanac.new_page(self.ensure_user)
        media_items = page.media
        c.media_items = h.render_media_items(media_items, editable=True)
        map_features = h.map_features_for_media(media_items)
        c.map_features = h.literal(simplejson.dumps(map_features))
        return render('/page/create.mako')

    def _do_create(self, almanac_slug):
        c.almanac = almanac = h.get_almanac_by_slug(almanac_slug)
        name = request.POST.get('name', u'')
        if not name:
            name = u'Unnamed'

        slug = h.name_page(almanac, name)
        page = c.almanac.new_page(self.ensure_user, name=name, slug=slug)

        meta.Session.commit()

        redirect_to(h.url_for('page_view', almanac=almanac, page=page))

    @dispatch_on(POST='_do_comment')
    def view(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        #XXX check permissions
        c.media_items = h.render_media_items(c.page.media, editable=True)
        map_features = h.map_features_for_media(c.page.media)
        c.map_features = h.literal(simplejson.dumps(map_features))
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
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        media_id_str = request.GET.get('media_id')
        if media_id_str:
            media_id = int(media_id_str.split('_')[-1])
            media_id -= 1
            media_items = h.get_session_media_items()
            media_item = media_items[media_id]
            c.text_value = media_item.text
        else:
            c.text_value = u''
        return dict(html=render('/media/story/form.mako'))

    @dispatch_on(POST='_do_form_map')
    @jsonify
    def form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        loc = c.almanac.location
        return dict(html=render('/media/map/form.mako'),
                    lat=loc.x, lng=loc.y,
                    )

    @jsonify
    def _do_form_text(self, almanac_slug):
        body = request.POST.get('body', u'')
        if not body:
            abort(400)
        c.almanac = h.get_almanac_by_slug(almanac_slug)

        media_id = request.POST.get('media_id')
        if media_id is None:
            c.story = story = Story()
            story.text = body

            media_items = h.get_session_media_items()
            story.order = len(media_items)
            media_items.append(story)
            session.save()
        else:
            try:
                media_id = int(media_id)
            except ValueError:
                abort(400)
            query = meta.Session.query(Story)
            query = query.filter(Story.id == media_id)
            #XXX error checking?
            c.story = query.one()
            c.story.text = body

        c.editable = True
        c.id = 'pagemedia_%d' % (c.story.id or len(media_items)-1)
        return dict(html=render('/media/story/item.mako'), id=c.id)

    @jsonify
    def _do_form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        json = request.POST.get('feature')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        # Stupid asShape returns a PointAdapter instead of a Point.  We round
        # trip it through wkb to get the correct type.
        location = wkb.loads(asShape(shape).to_wkb())

        c.map = map = Map()
        map.location = location
        media_items = h.get_session_media_items()
        map.order = len(media_items)
        media_items.append(map)
        session.save()

        c.editable = True
        c.id = 'pagemedia_%d' % (len(media_items)-1)
        return dict(html=render('/media/map/item.mako'),
                    map_id=c.id,
                    geometry=json,
                    )
