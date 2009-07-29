from communityalmanac.lib.base import BaseController, render
from formencode import Schema
from formencode import validators
from pylons import g
from pylons import config
from pylons import request
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
import communityalmanac.lib.helpers as h
import mailer

class ContactForm(Schema):
    name = validators.String()
    email = validators.Email(not_empty=True)
    message = validators.String(not_empty=True)

class ContactController(BaseController):

    @dispatch_on(POST='_do_contact')
    def contact(self):
        return render('/contact.mako')

    @validate(schema=ContactForm(), form='contact')
    def _do_contact(self):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        self._send_message(name, email, message)
        h.flash(u'Thank you for contacting us')
        redirect_to(h.url_for('home'))

    def _send_message(self, name, from_email, message):
        email = mailer.Message()
        if name:
            email.From = '%s <%s>' % (name, from_email)
            email.Subject = '[Almanac Support] A comment from %s' % name
        else:
            email.From = from_email
            email.Subject = '[Almanac Support] A comment'
        email.To = g.support_email
        email.Body = message
        if g.support_sending_enabled:
            server = mailer.Mailer(config['smtp_server'])
            server.send(email)
        else:
            print email.as_string()
