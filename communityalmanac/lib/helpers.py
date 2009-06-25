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
from communityalmanac.model import Video
from communityalmanac.model import meta
import lxml.html.clean
from pylons.controllers.util import abort
from pylons.templating import render_mako as render
from pylons import g
from pylons import request
from pylons import session
from pylons import tmpl_context as c
from routes.util import url_for
from sqlalchemy.orm import exc
from webhelpers.html import literal
from webhelpers.html.tags import checkbox
from webhelpers.html.tags import link_to
from webhelpers.html.tags import password
from webhelpers.paginate import Page as PaginationPage
from webhelpers.text import plural
import uuid

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

def get_page_by_id(page_id):
    try:
        return Page.by_id(page_id)
    except exc.NoResultFound:
        abort(404)

def sort_media_items(media, index_move, newsort):
    if index_move < 0 or index_move >= len(media):
        return False

    oldsort = media[index_move].order
    if oldsort > newsort:
        for item in media:
            if item.order == oldsort:
                item.order = newsort
            elif item.order >= newsort and item.order < oldsort:
                meta.Session.add(item)
                item.order += 1
    elif oldsort < newsort:
        for item in media:
            if item.order == oldsort:
                item.order = newsort
            elif item.order > oldsort and item.order <= newsort:
                meta.Session.add(item)
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
            new_uuid = str(uuid.uuid4())
            c.textarea_id = 'textarea_%s' % new_uuid
            c.textarea_class = 'mceSimple_%s' % new_uuid
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
        elif isinstance(media_item, Video):
            c.video = media_item
            rendered_item = render('/media/video/item.mako')
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
            geometry = media_item.location_4326.__geo_interface__
            map_id = 'pagemedia_%s' % (media_item.id or n)
            map_features.append(dict(map_id=map_id,
                                     geometry=geometry,
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

def clean_embed_markup(markup):
    allow_tags = g.allow_tags
    host_whitelist = g.host_whitelist

    cleaner = lxml.html.clean.Cleaner(remove_unknown_tags=False,
                                      whitelist_tags=allow_tags,
                                      host_whitelist=host_whitelist)
    return cleaner.clean_html(markup)

def clean_html(markup):
    return lxml.html.clean.clean_html(markup)

def flash(s):
    """add the string "s" to the session's flash store"""
    session.setdefault('flash', []).append(s)
    session.save()

def retrieve_flash_messages():
    """return a list of all the session's flash messages, and remove them from the session"""
    flash_messages = session.get('flash', None)
    if flash_messages is None:
        return []
    msgs = list(flash_messages)
    flash_messages[:] = []
    session.save()
    return msgs

def setup_pagination(collection, page=1, per_page=10):
    """set a number of "c" variables to allow for easy pagination in templates

    c.next_page_text, c.next_page_url
    c.prev_page_text, c.prev_page_url
    c.showing_start, c.showing_end
    c.items (this is the view of the current items in the collection)
    c.pagination (pagination object itself)
    """
    c.pagination = PaginationPage(collection, page=page, items_per_page=per_page)
    pd = pagination_data(c.pagination)
    if pd.get('next') is not None:
        start, end, page_idx = pd['next']
        c.next_page_text = '%d - %d' % (start, end)
        c.next_page_url = '%s?page=%s' % (request.path_url, page_idx)
    if pd.get('prev'):
        start, end, page_idx = pd['prev']
        c.prev_page_text = '%d - %d' % (start, end)
        c.prev_page_url = '%s?page=%s' % (request.path_url, page_idx)
    c.showing_start, c.showing_end = pd['showing']
    c.items = c.pagination.items
    return c.pagination

def pagination_data(pagination):
    """return a dictionary with the pagination data returned in a dict

    will have 3 keys, and the values will be a tuple with the start/end/page_idx
    dict(prev=(start, end, prev_page_id),
         next=(start, end, start_page_id),
         showing=(start, end),
         total=n,
         )
    """
    result = {}
    cur_page = pagination.page
    next_page = pagination.next_page
    prev_page = pagination.previous_page
    per_page = pagination.items_per_page
    if next_page:
        start = ((next_page-1) * per_page) + 1
        end = start + per_page - 1
        end = min(end, pagination.item_count)
        result['next'] = (start, end, next_page)
    if prev_page:
        start = (prev_page-1) * per_page
        end = (start + per_page - 1) + 1
        start = max(start, 1)
        result['prev'] = (start, end, prev_page)
    showing_start = ((cur_page-1) * per_page) + 1
    showing_end = cur_page * per_page
    showing_end = min(showing_end, pagination.item_count)
    result['showing'] = (showing_start, showing_end)
    result['total'] = pagination.item_count
    return result
