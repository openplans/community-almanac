import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
from communityalmanac.model import Almanac
from communityalmanac.model import meta

log = logging.getLogger(__name__)

class HomesweethomeController(BaseController):

    def home(self):
        c.almanacs = Almanac.latest()
        c.is_homepage = True
        return render('/home.mako')

