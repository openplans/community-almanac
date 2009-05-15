import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render

log = logging.getLogger(__name__)

class CommentController(BaseController):

    def form(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        return render('/comment/form.mako')
