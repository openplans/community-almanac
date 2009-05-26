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

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
from pylons.decorators.rest import dispatch_on
import communityalmanac.lib.helpers as h

log = logging.getLogger(__name__)

class MediaController(BaseController):

    @dispatch_on(GET='donothing')
    def sort(self):
        id = request.params.get('id')
        index = request.params.get('index')
        if not id or not index:
            abort(400)
        try:
            index = int(index)
            id = int(id.split('_')[-1])
        except ValueError:
            abort(400)
        if not h.sort_session_media_items(id, index):
            abort(400)
        # The only useful return value is the HTTP response, so we return an
        # empty body.
        return ''

    def donothing(self, almanac_slug):
        abort(400)

