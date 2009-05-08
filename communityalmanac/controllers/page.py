import logging

from communityalmanac.model import Page
from communityalmanac.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.rest import dispatch_on

from communityalmanac.lib.base import BaseController, render
import communityalmanac.lib.helpers as h

log = logging.getLogger(__name__)

class PageController(BaseController):

    @dispatch_on(POST='_do_create')
    def create(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        return render('/page/create.mako')

    def _do_create(self, almanac_slug):
        c.almanac = almanac = h.get_almanac_by_slug(almanac_slug)
        name = request.POST.get('name', u'')
        if not name:
            name = u'Unnamed'
        slug = h.name_page(almanac, name)
        page = Page(name, slug)
        almanac.pages.append(page)
        meta.Session.save(page)
        meta.Session.commit()
        # FIXME get the media items from the session
        # and attach it to the page
        redirect_to(h.url_for('page_view', almanac=almanac, page=page))

    def view(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        return render('/page/view.mako')

    @dispatch_on(POST='_do_form_text')
    def form_text(self, almanac_slug):
        return render('/page/form/text.mako')

    @dispatch_on(POST='_do_form_map')
    def form_map(self, almanac_slug):
        return render('/page/form/map.mako')

    def _do_form_text(self, almanac_slug):
        body = request.POST.get('body', u'')
        if not body:
            abort(400)
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        media_items = session.setdefault('media', [])
        session.save()
        return render('/page/item/text.mako')

    def _do_form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        return render('/page/item/map.mako')
