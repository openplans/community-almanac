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
from communityalmanac.model import Almanac
from communityalmanac.model import Audio
from communityalmanac.model import Image
from communityalmanac.model import Map
from communityalmanac.model import Media
from communityalmanac.model import PDF
from communityalmanac.model import Page
from communityalmanac.model import Story
from communityalmanac.model import meta
from pylons.controllers.util import abort
from pylons.templating import render_mako as render
from pylons import request
from pylons import session
from pylons import tmpl_context as c
from routes.util import url_for
from sqlalchemy.orm import exc
from webhelpers.html import literal
from webhelpers.html.tags import checkbox
from webhelpers.html.tags import link_to
from webhelpers.html.tags import password
import simplejson
import uuid

def normalize_url_slug(candidate):
    return candidate.replace(', ', '-').replace(' ', '').replace(',', '-')

def name_almanac(candidate):
    """name the almanac given the candidate name"""

    normalized = normalize_url_slug(candidate)
    try:
        Almanac.get_by_slug(normalized)
    except exc.NoResultFound:
        return normalized
    else:
        i = 1
        while True:
            name = '%s-%s' % (normalized, i)
            try:
                Almanac.get_by_slug(name)
                i += 1
            except exc.NoResultFound:
                return name

def name_page(almanac, candidate):
    """name the page given the almanac and candidate name"""

    normalized = normalize_url_slug(candidate)
    try:
        Page.get_by_slug(almanac, normalized)
    except exc.NoResultFound:
        return normalized
    else:
        i = 1
        while True:
            name = '%s-%s' % (normalized, i)
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

def get_media_by_id(media_id):
    try:
        return Media.by_id(media_id)
    except exc.NoResultFound:
        abort(404)

def sort_media_items(index_move, newsort):
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

def render_media_items(media_items, editable=False):
    """return a list of the rendered individual media items

    functions like these tend to balloon, so we should change our strategy if
    it gets complex"""

    from operator import itemgetter
    rendered_media_items = []

    c.editable = editable

    for index, media_item in enumerate(media_items):
        n = index + 1
        c.media_id = media_item.id or n
        if isinstance(media_item, Story):
            c.story = media_item
            rendered_item = render('/media/story/item.mako')
        elif isinstance(media_item, Map):
            c.map = media_item
            rendered_item = render('/media/map/item.mako')
        elif isinstance(media_item, Image):
            c.image = media_item
            rendered_item = render('/media/image/item.mako')
        elif isinstance(media_item, PDF):
            c.pdf = media_item
            rendered_item = render('/media/pdf/item.mako')
        elif isinstance(media_item, Audio):
            c.audio = media_item
            c.audio_url = request.application_url + c.audio.url
            c.flowplayer_id = 'pagemedia_%s' % c.audio.id
            rendered_item = render('/media/audio/item.mako')
        else:
            rendered_item = u''
        rendered_media_items.append((media_item.order, rendered_item))

    # We return the list sorted based on the media sort orders.
    return [rendered for sort, rendered in sorted(rendered_media_items, key=itemgetter(0))]

def map_features_for_media(media_items):
    """return a list of dicts that contain the features for all map media"""
    map_features = []
    for index, media_item in enumerate(media_items):
        n = index + 1
        if isinstance(media_item, Map):
            geometry = media_item.location.__geo_interface__
            geojson = simplejson.dumps(geometry)
            map_id = 'pagemedia_%s' % (media_item.id or n)
            map_features.append(dict(map_id=map_id,
                                     geometry=geojson,
                                     ))
    return map_features

def flowplayer_data_for_media(media_items):
    """return a list of dicts that contain the flowplayer data for all audio media"""
    flow_data = []
    for index, media_item in enumerate(media_items):
        n = index + 1
        if isinstance(media_item, Audio):
            flowplayer_id = 'pagemedia_%s' % media_item.id
            audio_url = request.application_url + media_item.url
            flow_data.append(dict(flowplayer_id=flowplayer_id,
                                  audio_url=audio_url,
                                  ))
    return flow_data
