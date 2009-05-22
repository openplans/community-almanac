import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.rest import dispatch_on
from pylons.decorators import validate
from formencode import Schema
from formencode import validators

from communityalmanac.lib.base import BaseController, render
import communityalmanac.lib.helpers as h
from communityalmanac.model import User
from communityalmanac.model import meta

log = logging.getLogger(__name__)

class UserRegistrationSchmema(Schema):
    login = validators.UnicodeString(min=5, not_empty=True)
    email_address = validators.Email(not_empty=True)
    password = validators.String(min=6, not_empty=True, encoding='utf8')
    password_repeat = validators.String(not_empty=True)
    chained_validators = [validators.FieldsMatch('password', 'password_repeat')]

class UserController(BaseController):

    def login(self):
        if request.environ.get('repoze.who.identity') == None:
            return render('/user/login.mako')
        redirect_to(h.url_for('home'))

    def logout(self):
        # The logout/forget process is handled by repoze.who.
        redirect_to(h.url_for('home'))

    @dispatch_on(POST='_register')
    def register(self):
        if request.environ.get('repoze.who.identity') == None:
            return render('/user/register.mako')
        redirect_to(h.url_for('home'))

    @validate(schema=UserRegistrationSchmema(), form='register')
    def _register(self):
        username = self.form_result['login']
        password = self.form_result['password']
        email_address = self.form_result['email_address']
        user = User(username, email_address, password)

        meta.Session.save(user)
        meta.Session.commit()

        # This is how we manually log in a user, as per repoze issue 58
        # http://bugs.repoze.org/issue58
        identity = {'repoze.who.userid': username}
        headers = request.environ['repoze.who.plugins']['auth_tkt'].remember(request.environ, identity)
        for k, v in headers:
            response.headers.add(k, v)

        redirect_to(h.url_for('home'))

    def test(self):
        if request.environ.get('repoze.who.identity') == None:
            abort(401)
        return 'Success'
