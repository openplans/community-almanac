from __future__ import with_statement
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.rest import dispatch_on
from pylons.decorators import validate
from formencode import Schema
from formencode import validators
from formencode import compound

from communityalmanac.lib.base import BaseController, render
import communityalmanac.lib.helpers as h
from communityalmanac.model import User
from communityalmanac.model import meta
from sqlalchemy import or_, and_
from os import path
import mailer
import re

log = logging.getLogger(__name__)
STYLE_URL = re.compile(r"""url\("(.*?)"\)|url\('(.*?)'\)|url\((.*?)\)""")

class UserRegistrationSchema(Schema):
    login = validators.UnicodeString(min=5, not_empty=True)
    email_address = validators.Email(not_empty=True)
    password = validators.String(min=6, not_empty=True, encoding='utf8')
    password_repeat = validators.String(not_empty=True)
    chained_validators = [validators.FieldsMatch('password', 'password_repeat')]

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

    @validate(schema=UserRegistrationSchema(), form='register')
    def _register(self):
        username = self.form_result['login']
        password = self.form_result['password']
        email_address = self.form_result['email_address']
        user = User(username, email_address, password)

        meta.Session.save(user)
        meta.Session.commit()

        self._login(username)

        redirect_to(h.url_for('home'))

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
        user = meta.Session.query(User).filter(or_(User.username==login, User.email_address==login)).one()
        user.generate_key()
        meta.Session.commit()

        message = mailer.Message()
        message.From = "noreply@%s" % "communityalmanac.org"
        message.To = user.email_address
        message.Subject = "Community Almanac account details"
        message.Body, message.Html = self._email_strip(render('/user/account_email.mako'), message)
        emailc = {}
        #server = mailer.Mailer('mail.openplans.org')
        server = mailer.Mailer('localhost:2000')
        server.send(message)

        redirect_to(h.url_for('home'))

    def _email_strip(self, html, message):
        # Todo, remove javascript, strip extra white space...
        import lxml.html
        doc = lxml.html.fromstring(html)
        login_form = doc.cssselect("form#login_form")
        # Remove the login form (all forms?)
        for form in login_form:
            form.getparent().remove(form)

        # Remove the javascript
        for script in doc.cssselect('script'):
            script.getparent().remove(script)

        if not hasattr(self, '__embedded_images'):
            self.__embedded_images = {}
        # Embed images
        for image in doc.cssselect('img'):
            location = image.attrib['src']
            filepath = path.abspath(path.join(__file__, '../../public', './%s' % location))
            filename = path.basename(filepath)
            if filepath not in self.__embedded_images:
                self.__embedded_images[filepath] = filename
                message.attach(filepath, filename)
            image.attrib['src'] = 'cid:%s' % filename

        for sidebar in doc.cssselect('.sidebar'):
            sidebar.getparent().remove(sidebar)

        #embed stylesheets
        for stylesheet in doc.cssselect('link[rel=stylesheet]'):
            head = stylesheet.getparent()
            location = stylesheet.attrib['href']
            filepath = path.join(__file__, '../../public', './%s' % location)
            try:
                with open(path.abspath(filepath)) as stylefile:
                    styledata = stylefile.read()
            except:
                continue

            styledata = self.__style_fixup(styledata, message)
            head.remove(stylesheet)
            head.append(lxml.html.fromstring("""<style type="text/css" media="screen">%s</style>""" % styledata))

        # Fixup embedded styles
        for element in doc.iter():
            if 'style' in element.attrib:
                element.attrib['style'] = self.__style_fixup(element.attrib['style'], message)
        # We need to take the text content from the body
        body = doc.cssselect('body')[0]
        text_content = body.text_content().encode('utf8')
        return text_content, lxml.html.tostring(doc).encode('utf8')

    def __style_fixup(self, styledata, message):
        if not hasattr(self, '__embedded_images'):
            self.__embedded_images = {}
        def image_embed(matchobj):
            filepath = path.abspath(path.join(__file__, '../../public', './%s' % (matchobj.group(1) or matchobj.group(2) or matchobj.group(3))))
            try:
                with open(path.abspath(filepath)) as stylefile:
                    pass
            except:
                return matchobj.group(0)
            filename = path.basename(filepath)
            if filepath not in self.__embedded_images:
                self.__embedded_images[filepath] = filename
                message.attach(filepath, filename)
            return "url(cid:%s)" % filename
        return re.sub(STYLE_URL, image_embed, styledata)

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
        user = meta.Session.query(User).filter(and_(User.username==username, User.reset_key==key)).one()
        user.reset_key = None
        if password:
            user.set_password(password)
        meta.Session.commit()
        self._login(username)

        redirect_to(h.url_for('home'))

    def test(self):
        if request.environ.get('repoze.who.identity') == None:
            abort(401)
        return 'Success'
