import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.rest import dispatch_on

from communityalmanac.lib.base import BaseController, render
import communityalmanac.lib.helpers as h

log = logging.getLogger(__name__)

class UserController(BaseController):

    def login(self):
        # Return a rendered template
        #return render('/users.mako')
        # or, return a response
        if request.environ.get('repoze.who.identity') == None:
            return render('/login.mako')
        redirect_to(h.url_for('home'))

    def logout(self):
        redirect_to(h.url_for('home'))

    @dispatch_on(POST='_register'):
    def register(self):
        pass

    def _register(self):
        pass

    def test(self):
        if request.environ.get('repoze.who.identity') == None:
            abort(401)
        return 'Success'
