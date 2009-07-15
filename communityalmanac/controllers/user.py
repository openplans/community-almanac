from __future__ import with_statement
import logging

from pylons import request, response, session, tmpl_context as c
from pylons import config
from pylons.controllers.util import abort, redirect_to, redirect
from pylons.decorators.rest import dispatch_on
from pylons.decorators import validate
from formencode import Schema
from formencode import validators
from formencode import compound

from communityalmanac.lib.base import BaseController, render
import communityalmanac.lib.helpers as h
from communityalmanac.model import FullUser
from communityalmanac.model import meta
from sqlalchemy import or_, and_, exc
from sqlalchemy.sql import func
import mailer
from formencode.htmlfill import none_formatter

log = logging.getLogger(__name__)

class UniqueUsername(validators.FancyValidator):

     messages = {
         'duplicate': 'This username is already taken.'
         }

     def validate_python(self, value, state):
         count = meta.Session.query(func.count()).filter(FullUser.username==value).all()[0][0]
         if count:
             raise validators.Invalid(self.message("duplicate", state), value, state)

class UniqueEmail(validators.Email):

     messages = {
         'duplicate': 'A user already exists with this email. Have you <a href="%s">forgotten your password?</a>' % h.url_for('user_requestreset')
         }

     def validate_python(self, value, state):
         count = meta.Session.query(func.count()).filter(FullUser.email_address==value).all()[0][0]
         if count:
             raise validators.Invalid(self.message("duplicate", state), value, state)

def pass_html_error_formatter(error):
    return '<span class="error-message">%s</span><br />\n' % error

class UserRegistrationSchema(Schema):
    register_login = UniqueUsername()
    register_email_address = UniqueEmail(not_empty=True)
    register_password = validators.String(not_empty=True, encoding='utf8')
    register_password_repeat = validators.String(not_empty=True)
    came_from = validators.String(not_empty=False)
    chained_validators = [validators.FieldsMatch('register_password', 'register_password_repeat')]

class RequestResetSchema(Schema):
    login = compound.Any(validators.UnicodeString(min=5, not_empty=True), validators.Email(not_empty=True))

class PerformResetSchema(Schema):
    username = validators.UnicodeString(min=5, not_empty=True)
    key = validators.String(min=5, not_empty=True)
    password = validators.String(encoding='utf8')
    password_repeat = validators.String()
    chained_validators = [validators.FieldsMatch('password', 'password_repeat')]

class UserController(BaseController):

    def login(self):
        c.active_section = request.params.get('show','login-new')
        if request.environ.get('repoze.who.identity') == None:
            return render('/user/login.mako')
        redirect(request.params.get('came_from', h.url_for('home')))

    def logout(self):
        # The logout/forget process is handled by repoze.who.
        redirect_to(h.url_for('home'))

    @dispatch_on(POST='_register')
    def register(self):
        if request.environ.get('repoze.who.identity') == None:
            c.active_section = request.params.get('show','login-new')
            return render('/user/login.mako')
        h.flash(u'Unable to register as a user is already logged in.  Please logout first.')
        redirect_to(h.url_for('home'))

    @validate(schema=UserRegistrationSchema(), form='register', auto_error_formatter=pass_html_error_formatter)
    def _register(self):
        username = self.form_result['register_login']
        password = self.form_result['register_password']
        email_address = self.form_result['register_email_address']
        user = FullUser(username, email_address, password)

        meta.Session.save(user)
        try:
            meta.Session.commit()
        except exc.IntegrityError:
            # User exists already, and we hit a race condition.  We re-validate
            # the schema so that FormEncode will display a proper error
            # message.
            schema = UserRegistrationSchema()
            try:
                form_result = schema.to_python(request.params)
            except validators.Invalid, error:
                c.form_result = error.value
                c.form_errors = error.error_dict or {}
                c.active_section = request.params.get('show','login-new')
                return render('/user/login.mako')

        self._login(username)

        redirect(request.params.get('came_from', h.url_for('home')))

    def _login(self, username):
        # This is how we manually log in a user, as per repoze issue 58
        # http://bugs.repoze.org/issue58
        identity = {'repoze.who.userid': username}
        headers = request.environ['repoze.who.plugins']['auth_tkt'].remember(request.environ, identity)
        for k, v in headers:
            response.headers.add(k, v)

    @dispatch_on(POST='_request_reset')
    def request_reset(self):
        return render('/user/request_reset.mako')

    @validate(schema=RequestResetSchema(), form='request_reset')
    def _request_reset(self):
        login = self.form_result['login']
        user = meta.Session.query(FullUser).filter(or_(FullUser.username==login, FullUser.email_address==login)).one()
        user.generate_key()
        meta.Session.commit()

        c.username = user.username
        c.key = user.reset_key

        message = mailer.Message()
        message.From = "Community Alamanc <noreply@%s>" % "communityalmanac.org"
        message.To = user.email_address
        message.Subject = "Community Almanac account details"
        message.Body, message.Html = self._email_strip(render('/email/account_details.mako'), message)
        server = mailer.Mailer(config['smtp_server'])
        server.send(message)

        h.flash(u'A password reset has been sent. Please check your email.')
        redirect_to(h.url_for('home'))

    @dispatch_on(POST='_perform_reset')
    def perform_reset(self, username, key):
        return render('/user/perform_reset.mako')

    def _perform_reset(self, username, key):
        myparams = dict(request.params)
        myparams['username'] = username
        myparams['key'] = key
        schema = PerformResetSchema()
        try:
            form_result = schema.to_python(myparams)
        except validators.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            return render('/user/perform_reset.mako')
        password = form_result['password']
        user = meta.Session.query(FullUser).filter(and_(FullUser.username==username, FullUser.reset_key==key)).one()
        user.reset_key = None
        if password:
            user.set_password(password)
        meta.Session.commit()
        self._login(username)

        h.flash(u'Your password has been reset')
        redirect_to(h.url_for('home'))

    def test(self):
        if request.environ.get('repoze.who.identity') == None:
            abort(401)
        return 'Success'
