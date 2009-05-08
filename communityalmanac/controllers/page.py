import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
import communityalmanac.lib.helpers as h

log = logging.getLogger(__name__)

class PageController(BaseController):

    def create(self, almanac_slug):
        almanac = h.get_almanac_by_slug(almanac_slug)
        return render('/page/create.mako')

    def view(self, almanac_slug, page_slug):
        almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(almanac, page_slug)
        return render('/page/view.mako')

    def form_text(self):
        return render('/page/form/text.mako')

    def form_map(self):
        return render('/page/form/map.mako')
