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
from communityalmanac.model import Story
from pylons.decorators import jsonify
from pylons.decorators.rest import dispatch_on
import communityalmanac.lib.helpers as h

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
        if not h.sort_session_media_items(id, index):
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
    def _do_new_form_text(self):
        body = request.POST.get('body', u'')
        if not body:
            abort(400)

        c.story = story = Story()
        story.text = body

        media_items = h.get_session_media_items()
        story.order = len(media_items)
        media_items.append(story)
        session.save()

        c.editable = True
        c.media_id = c.story.id or len(h.get_session_media_items())
        return dict(html=render('/media/story/item.mako'))

    @dispatch_on(POST='_do_edit_form_text')
    @jsonify
    def edit_form_text(self, media_id):
        c.story = h.get_media_from_session(media_id)
        c.media_id = media_id
        return dict(html=render('/media/story/form.mako'))

    @jsonify
    def _do_edit_form_text(self, media_id):
        body = request.POST.get('body', u'')
        if not body:
            abort(400)

        #XXX hard coded get from session
        c.story = h.get_media_from_session(media_id)
        c.story.text = body
        session.save()

        c.editable = True
        c.media_id = media_id
        return dict(html=render('/media/story/item.mako'))

    @jsonify
    def text_view(self, media_id):
        c.editable = True
        # XXX we'll need a way to figure out if we want to get the item from the
        # session or the database, maybe through a request variable? or maybe
        # we'll have separate urls
        # for now, we'll just assume session
        c.story = h.get_media_from_session(media_id)
        c.media_id = media_id
        return dict(html=render('/media/story/item.mako'))

    @jsonify
    def delete_text(self, media_id):
        #XXX hardcoded to use session
        try:
            media_id = int(media_id)
            media_id -= 1
            media_items = h.get_session_media_items()
            del media_items[media_id]
            session.save()
        except (ValueError, IndexError):
            abort(400)
        return {}

    def clear_session(self):
        # XXX debug only
        session.clear()
        session.save()
