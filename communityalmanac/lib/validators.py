# Community Almanac - A place for your stories.
# Copyright (C) 2009  Douglas Mayle, Robert Marianski,
# Andy Cochran, Chris Patterson

# This file is part of Community Almanac.

# Community Almanac is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Community Almanac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Community Almanac.  If not, see <http://www.gnu.org/licenses/>.

import logging
from formencode import validators
from pylons import g
import recaptcha.client.captcha


log = logging.getLogger(__name__)

class RecaptchaValidator(validators.FancyValidator):
    messages = {
        'invalid': u'Please enter both words'
        }

    def validate_python(self, field_dict, state):
        if not g.captcha_enabled:
            return

        def do_invalid():
            errormsg = self.message('invalid', state)
            errors = {'recaptcha_marker_field': errormsg}
            raise validators.Invalid(errormsg, field_dict, state, error_dict=errors)

        try:
            captcha_challenge = field_dict['recaptcha_challenge_field']
            captcha_response = field_dict['recaptcha_response_field']
        except KeyError, e:
            do_invalid()

        recaptcha_response = recaptcha.client.captcha.submit(captcha_challenge, captcha_response, g.captcha_privkey, '127.0.0.1')
        log.info('Recaptcha was valid: %r' % recaptcha_response.is_valid)
        if not recaptcha_response.is_valid:
            do_invalid()


class AkismetValidator(validators.FancyValidator):
    messages = {
        'spam': u'Your comment appears to be spam.'
        }

    def validate_python(self, field_dict, state):
        if not g.akismet_enabled:
            log.info("akismet disabled")
            return

        def do_invalid():
            log.info("akismet caught possible spam")
            errormsg = self.message('spam', state)
            errors = {'text': errormsg}
            raise validators.Invalid(errormsg, field_dict, state, error_dict=errors)

        import akismet
        ak = akismet.Akismet(key=g.akismet_key, blog_url=g.akismet_url)

        try:
            ak.verify_key()
        except akismet.APIKeyError, e:
            log.error("Invalid akismet key, can't filter spam")
            return
        except:
            import traceback
            msg = traceback.format_exc()
            log.error(msg)
            return

        comment = field_dict['text']
        import os
        data = {'comment_author': field_dict.get('fullname'),
                'comment_author_url': field_dict.get('website'),
                'comment_author_email': field_dict.get('email'),
                'user_ip': os.environ.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': os.environ.get('HTTP_USER_AGENT', ''),
                }
        # A lot of spam is not ASCII.
        # But if we feed extended characters to ak.comment_check(),
        # then it blows up because urllib.urlencode() needs everything
        # to pass through str().  So, encode first.
        comment = comment.encode('utf8')
        for key, val in data.items():
            data[key] = val.encode('utf8')

        try:
            is_spam = ak.comment_check(comment, data=data, build_data=True)
        except:
            import traceback
            msg = traceback.format_exc()
            log.error(msg)
            is_spam = False

        if is_spam:
            do_invalid()
        else:
            log.info("akismet says message is OK")
