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

"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from communityalmanac.model import Almanac
from communityalmanac.model import Page
from communityalmanac.model import meta
from pylons.controllers.util import abort
from routes.util import url_for
from sqlalchemy.orm import exc
from webhelpers.html.tags import checkbox
from webhelpers.html.tags import link_to
from webhelpers.html.tags import password

def name_almanac(candidate):
    """name the almanac given the candidate name"""

    try:
        Almanac.get_by_slug(candidate)
    except exc.NoResultFound:
        return candidate
    else:
        i = 1
        while True:
            name = '%s-%s' % (candidate, i)
            try:
                Almanac.get_by_slug(name)
                i += 1
            except exc.NoResultFound:
                return name

def get_almanac_by_slug(almanac_slug):
    try:
        return Almanac.get_by_slug(almanac_slug)
    except exc.NoResultFound:
        abort(404)

def get_page_by_slug(almanac, page_slug):
    try:
        return Page.get_by_slug(almanac, page_slug)
    except exc.NoResultFound:
        abort(404)
