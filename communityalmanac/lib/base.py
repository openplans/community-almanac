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

"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from communityalmanac.model import meta
from pylons.controllers.util import redirect_to
from urlparse import urlunparse

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

    def __before__(self, *args, **kwargs):
        environ = kwargs.get('environ', {})
        # We only support one key, currently, so we must make sure that the
        # server is accessed correctly.
        hostport = environ.get('HTTP_HOST', ':')
        server = '%s:%s' % (environ.get('SERVER_NAME'), environ.get('SERVER_PORT'))

        if hostport != server:
            redirect_url = urlunparse(('http', server, environ.get('PATH_INFO'), '', environ.get('QUERY_STRING'), ''))
            redirect_to(redirect_url)
