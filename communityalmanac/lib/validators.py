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
        log.debug('Recaptcha was valid: %r' % recaptcha_response.is_valid)
        if not recaptcha_response.is_valid:
            do_invalid()

