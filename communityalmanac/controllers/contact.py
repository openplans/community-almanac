from communityalmanac.lib.base import BaseController, render
from formencode import Schema
from formencode import validators
from pylons import g
from pylons import request
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
import communityalmanac.lib.helpers as h
import email.utils
import smtplib

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
        headers = {}
        if name:
            from_addr = '%s <%s>' % (name, from_email)
            headers['Subject'] = '[Almanac Support] A comment from %s' % name
        else:
            from_addr = from_email
            headers['Subject'] = '[Almanac Support] A comment'
        headers['To'] = g.support_email
        headers['From'] = from_addr
        headers['Content-Type'] = 'text/plain'
        headers['Date'] = email.utils.formatdate()
        email_message = '\n'.join('%s: %s' % (k, v) for k, v in headers.items())
        email_message += '\n\n' + message
        if g.email_sending_enabled:
            mail_session = smtplib.SMTP(g.smtp_host, g.smtp_port)
            mail_session.sendmail(from_email, [g.support_email], email_message)
        else:
            print email_message
