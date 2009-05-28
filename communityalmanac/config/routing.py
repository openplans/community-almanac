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

"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper
from formalchemy.ext.pylons import maps

def almanac_expand(kw):
    if 'almanac' in kw:
        almanac = kw['almanac']
        kw['almanac_slug'] = almanac.slug
        del kw['almanac']
    return kw

def page_expand(kw):
    kw = almanac_expand(kw)
    if 'page' in kw:
        page = kw['page']
        kw['page_slug'] = page.slug
        del kw['page']
    return kw

def media_expand(kw):
    if 'media' in kw:
        media = kw['media']
        kw['media_id'] = media.id
        del kw['media']
    return kw

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    maps.admin_map(map, controller='admin', url='/admin')

    map.connect('home', '/', controller='almanac', action='home')
    # FIXME not sure if we should keep this url scheme
    map.connect('login', '/login', controller='user', action='login')
    map.connect('user_register', '/signup', controller='user', action='register')
    map.connect('user_requestreset', '/forgot', controller='user', action='request_reset')
    map.connect('user_performreset', '/reset/{username}/{key}', controller='user', action='perform_reset')
    map.connect('test', '/test', controller='user', action='test')
    map.connect('session_sort', '/sort', controller='media', action='sort')
    map.connect('almanac_center', '/api/center/:almanac_slug', controller='almanac', action='center', _filter=almanac_expand)
    map.connect('kml', '/api/kml/:almanac_slug', controller='almanac', action='kml', _filter=almanac_expand)
    map.connect('geocode', '/api/geocode', controller='geocoder', action='geocode')
    map.connect('page_create', '/:almanac_slug/+page', controller='page', action='create', _filter=almanac_expand)
    map.connect('page_view', '/:almanac_slug/:page_slug', controller='page', action='view', _filter=page_expand)
    map.connect('almanac_create', '/+almanac', controller='almanac', action='create')
    map.connect('almanac_view', '/:almanac_slug', controller='almanac', action='view', _filter=almanac_expand)

    map.connect('media_story_new', '/media/text/new', controller='media', action='new_form_text')
    map.connect('media_story_view', '/media/text/:media_id', controller='media', action='text_view', _filter=media_expand)
    map.connect('media_story_edit', '/media/text/edit/:media_id', controller='media', action='edit_form_text', _filter=media_expand)
    map.connect('media_story_delete', '/media/text/delete/:media_id', controller='media', action='delete_text', conditions=dict(method=['POST']), _filter=media_expand)

    # XXX debug only
    map.connect('clear_session', '/clear/my/session', controller='media', action='clear_session')


    return map
