import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AlmanacController(BaseController):

    def home(self):
        # Return a rendered template
        #return render('/almanac.mako')
        # or, return a response
        return render('/home.mako')
