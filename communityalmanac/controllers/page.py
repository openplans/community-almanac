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
from formencode.compound import Any
from formencode import Schema
from formencode import validators
from pylons import request, response, session, tmpl_context as c
from pylons import g
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from repoze.what.predicates import not_anonymous
from communityalmanac.lib.auths import is_page_owner
from repoze.what.plugins.pylonshq import ActionProtector
from communityalmanac.lib.base import BaseController, render
from shapely.geometry.geo import asShape
from shapely import wkb
import communityalmanac.lib.helpers as h
import recaptcha.client.captcha
import simplejson

log = logging.getLogger(__name__)

class LoggedInValidator(validators.FancyValidator):
    messages = {
        'invalid': 'must be logged in'
        }

    def validate_python(self, value, state):
        if not c.user:
            raise validators.Invalid(self.message('invalid', state), value, state)

class RecaptchaValidator(validators.FancyValidator):
    messages = {
        'invalid': u'Please enter both words'
        }

    def validate_python(self, field_dict, state):
        if not g.captcha_enabled:
            return

        def do_invalid():
            errormsg = self.message('invalid', state)
            errors = {'recaptcha_marker_field': errormsg}
            raise validators.Invalid(errormsg, field_dict, state, error_dict=errors)

        try:
            captcha_challenge = field_dict['recaptcha_challenge_field']
            captcha_response = field_dict['recaptcha_response_field']
        except KeyError, e:
            do_invalid()

        recaptcha_response = recaptcha.client.captcha.submit(captcha_challenge, captcha_response, g.captcha_privkey, '127.0.0.1')
        if not recaptcha_response.is_valid:
            do_invalid()


class PageCommentForm(Schema):
    fullname = validators.String(not_empty=True)
    email = validators.Email(not_empty=True)
    website = validators.String()
    text = validators.String(not_empty=True)
    chained_validators = [Any(RecaptchaValidator(), LoggedInValidator())]
    allow_extra_fields = True


class PageController(BaseController):

    @dispatch_on(POST='_do_publish')
    def create(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = page = c.almanac.new_page(self.ensure_user)
        media_items = page.media
        c.media_items = h.render_media_items(media_items, editable=True)
        map_features = h.map_features_for_media(media_items)
        c.map_features = h.literal(simplejson.dumps(map_features))
        flow_data = h.flowplayer_data_for_media(media_items)
        c.flow_data = h.literal(simplejson.dumps(flow_data))
        c.is_add = True
        c.behalf = render('/page/behalf.mako')
        return render('/page/add_edit.mako')

    @ActionProtector(not_anonymous())
    def _do_publish(self, almanac_slug):
        c.almanac = almanac = h.get_almanac_by_slug(almanac_slug)
        name = request.POST.get('name', u'')
        if not name:
            name = u'Unnamed'

        slug = Page.name_page(almanac, name)
        page = c.almanac.new_page(self.ensure_user, name=name, slug=slug)
        page.published = True

        meta.Session.commit()

        h.flash(u'Page created')
        redirect_to(h.url_for('page_view', almanac=almanac, page=page))

    @dispatch_on(POST='_do_comment')
    def view(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.media_items = h.render_media_items(c.page.media, editable=False)
        map_features = h.map_features_for_media(c.page.media)
        c.map_features = h.literal(simplejson.dumps(map_features))
        flow_data = h.flowplayer_data_for_media(c.page.media)
        c.flow_data = h.literal(simplejson.dumps(flow_data))

        page_navigation = c.page.page_navigation()
        c.next_page = page_navigation['next']
        c.prev_page = page_navigation['prev']
        c.latest_pages = Page.latest(almanac_id=c.almanac.id)
        if g.captcha_enabled and not c.user:
            c.captcha_html = h.literal(recaptcha.client.captcha.displayhtml(g.captcha_pubkey))
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
        h.flash(u'Comment added')
        redirect_to(h.url_for('page_view', almanac=almanac, page=page))

    @dispatch_on(POST='_do_edit')
    def edit(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.media_items = h.render_media_items(c.page.media, editable=True)
        map_features = h.map_features_for_media(c.page.media)
        c.map_features = h.literal(simplejson.dumps(map_features))
        flow_data = h.flowplayer_data_for_media(c.page.media)
        c.flow_data = h.literal(simplejson.dumps(flow_data))
        c.is_add = False
        c.behalf = render('/page/behalf.mako')
        return render('/page/add_edit.mako')

    @ActionProtector(is_page_owner())
    def _do_edit(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        name = request.POST.get('name', u'')
        if name:
            # all we have to save is the name here for now
            c.page.name = name
            meta.Session.commit()
        h.flash(u'Page edited')
        redirect_to(h.url_for('page_view', almanac=c.almanac, page=c.page))

    def on_behalf_of(self, page_id):
        c.page = h.get_page_by_id(page_id)
        return render('/page/behalf.mako')

    @dispatch_on(POST='_do_on_behalf_of_form')
    def on_behalf_of_form(self, page_id):
        c.page = h.get_page_by_id(page_id)
        return render('/page/behalf-form.mako')

    #XXX getting almanac_slug error here
    #@ActionProtector(is_page_owner())
    def _do_on_behalf_of_form(self, page_id):
        c.page = h.get_page_by_id(page_id)
        on_behalf_of = request.POST.get('on_behalf_of')
        if on_behalf_of is None:
            abort(400)
        c.page.on_behalf_of = on_behalf_of
        meta.Session.commit()
        return render('/page/behalf.mako')

    def all_pages_kml(self, query):
        c.pages = Page.search_all(query).all()
        response.content_type = 'application/vnd.google-earth.kml+xml kml'
        return render('/page/kml.mako')

    def all_pages(self, query):
        c.pages = Page.search_all(query).all()
        return render('/page/kml.mako')
