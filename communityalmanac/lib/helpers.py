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
from communityalmanac.lib.base import render
from communityalmanac.model import Almanac
from communityalmanac.model import Page
from communityalmanac.model import Story
from communityalmanac.model import meta
from pylons.controllers.util import abort
from pylons import session
from routes.util import url_for
from sqlalchemy.orm import exc
from webhelpers.html import literal
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

def name_page(almanac, candidate):
    """name the page given the almanac and candidate name"""

    try:
        Page.get_by_slug(almanac, candidate)
    except exc.NoResultFound:
        return candidate
    else:
        i = 1
        while True:
            name = '%s-%s' % (candidate, i)
            try:
                Page.get_by_slug(almanac, name)
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

def get_session_media_items():
    media_items = session.setdefault('media', [])
    return media_items

def sort_session_media_items(index_move, newsort):
    media = get_session_media_items()

    if index_move < 0 or index_move >= len(media):
        return False

    oldsort = media[index_move].order
    if oldsort > newsort:
        for item in media:
            if item.order == oldsort:
                item.order = newsort
            elif item.order >= newsort and item.order < oldsort:
                item.order += 1
    elif oldsort < newsort:
        for item in media:
            if item.order == oldsort:
                item.order = newsort
            elif item.order > oldsort and item.sort <= newsort:
                item.order -= 1
    return True

def remove_session_media_items():
    media_items = session.pop('media', [])
    session.save()
    return media_items

def render_media_items(media_items):
    """return a list of the rendered individual media items

    functions like these tend to balloon, so we should change our strategy if
    it gets complex"""

    from operator import itemgetter
    rendered_media_items = []

    for index, media_item in enumerate(media_items):
        rendered_story = render('/media/%s/item.mako' % media_item.__class__.__name__.lower(),
            extra_vars=dict(story=media_item, id='pagemedia_%d' % (media_item.id or index)))
        rendered_media_items.append((media_item.order, rendered_story))

    # We return the list sorted based on the media sort orders.
    return [rendered for sort, rendered in sorted(rendered_media_items, key=itemgetter(0))]
