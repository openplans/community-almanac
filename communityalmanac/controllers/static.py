from communityalmanac.lib.base import BaseController, render
from communityalmanac.model import Page
from pylons import tmpl_context as c

class StaticController(BaseController):
    def about(self):
        c.no_maps = True
        c.latest_pages = Page.latest()
        return render('/about.mako')

    def badges(self):
        c.no_maps = True
        return render('/badges.mako')
