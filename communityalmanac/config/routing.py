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
        kw['filename'] = media.filename
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

    map.connect('home', '/', controller='homesweethome', action='home')
    map.connect('almanacs_kml', '/api/kml/almanacs', controller='homesweethome', action='almanacs_kml')
    map.connect('pages_kml', '/api/kml/:almanac_slug/pages', controller='almanac', action='pages_kml', _filter=almanac_expand)
    # FIXME not sure if we should keep this url scheme
    map.connect('login', '/login', controller='user', action='login')
    map.connect('user_register', '/signup', controller='user', action='register')
    map.connect('user_requestreset', '/forgot', controller='user', action='request_reset')
    map.connect('user_performreset', '/reset/{username}/{key}', controller='user', action='perform_reset')
    map.connect('test', '/test', controller='user', action='test')
    map.connect('media_item_sort', '/api/sort/:almanac_slug/:page_slug', controller='media', action='sort', conditions=dict(method=['POST']), _filter=page_expand)
    map.connect('media_item_temppage_sort', '/api/sort/:almanac_slug', controller='media', action='temppage_sort', conditions=dict(method=['POST']), _filter=almanac_expand)
    map.connect('almanac_center', '/api/center/:almanac_slug', controller='almanac', action='center', _filter=almanac_expand)
    map.connect('geocode', '/api/geocode', controller='geocoder', action='geocode')
    map.connect('page_create', '/:almanac_slug/+page', controller='page', action='create', _filter=almanac_expand)
    map.connect('page_view', '/:almanac_slug/:page_slug', controller='page', action='view', _filter=page_expand)
    map.connect('page_edit', '/:almanac_slug/:page_slug/edit', controller='page', action='edit', _filter=page_expand)
    map.connect('almanac_create', '/+almanac', controller='almanac', action='create')
    map.connect('almanac_view', '/:almanac_slug', controller='almanac', action='view', _filter=almanac_expand)

    # media item routes
    map.connect('media_story_new', '/media/text/:almanac_slug/new', controller='media', action='new_form_text', _filter=almanac_expand)
    map.connect('media_story_existing_new', '/media/text/:almanac_slug/:page_slug/new', controller='media', action='new_form_existing_text', _filter=page_expand)
    map.connect('media_story_view', '/media/text/:media_id', controller='media', action='text_view', _filter=media_expand)
    map.connect('media_story_edit', '/media/text/edit/:media_id', controller='media', action='edit_form_text', _filter=media_expand)
    map.connect('media_story_delete', '/media/text/delete/:media_id', controller='media', action='delete_text', conditions=dict(method=['POST']), _filter=media_expand)

    map.connect('media_map_new', '/media/map/:almanac_slug/new', controller='media', action='new_form_map', _filter=almanac_expand)
    map.connect('media_map_existing_new', '/media/map/:almanac_slug/:page_slug/new', controller='media', action='new_form_existing_map', _filter=page_expand)
    map.connect('media_map_view', '/media/map/:media_id', controller='media', action='map_view', _filter=media_expand)
    map.connect('media_map_edit', '/media/map/edit/:media_id', controller='media', action='edit_form_map', _filter=media_expand)
    map.connect('media_map_delete', '/media/map/delete/:media_id', controller='media', action='delete_map', conditions=dict(method=['POST']), _filter=media_expand)

    map.connect('media_image_new', '/media/image/:almanac_slug/new', controller='media', action='new_form_image', _filter=almanac_expand)
    map.connect('media_image_existing_new', '/media/image/:almanac_slug/:page_slug/new', controller='media', action='new_form_existing_image', _filter=page_expand)
    map.connect('media_image_view', '/media/image/:media_id', controller='media', action='image_view', _filter=media_expand)
    map.connect('media_image_edit', '/media/image/edit/:media_id', controller='media', action='edit_form_image', _filter=media_expand)
    map.connect('media_image_delete', '/media/image/delete/:media_id', controller='media', action='delete_image', conditions=dict(method=['POST']), _filter=media_expand)

    map.connect('media_pdf_new', '/media/pdf/:almanac_slug/new', controller='media', action='new_form_pdf', _filter=almanac_expand)
    map.connect('media_pdf_existing_new', '/media/pdf/:almanac_slug/:page_slug/new', controller='media', action='new_form_existing_pdf', _filter=page_expand)
    map.connect('media_pdf_view', '/media/pdf/:media_id', controller='media', action='pdf_view', _filter=media_expand)
    map.connect('media_pdf_edit', '/media/pdf/edit/:media_id', controller='media', action='edit_form_pdf', _filter=media_expand)
    map.connect('media_pdf_delete', '/media/pdf/delete/:media_id', controller='media', action='delete_pdf', conditions=dict(method=['POST']), _filter=media_expand)

    map.connect('media_audio_new', '/media/audio/:almanac_slug/new', controller='media', action='new_form_audio', _filter=almanac_expand)
    map.connect('media_audio_existing_new', '/media/audio/:almanac_slug/:page_slug/new', controller='media', action='new_form_existing_audio', _filter=page_expand)
    map.connect('media_audio_view', '/media/audio/:media_id', controller='media', action='audio_view', _filter=media_expand)
    map.connect('media_audio_edit', '/media/audio/edit/:media_id', controller='media', action='edit_form_audio', _filter=media_expand)
    map.connect('media_audio_delete', '/media/audio/delete/:media_id', controller='media', action='delete_audio', conditions=dict(method=['POST']), _filter=media_expand)

    map.connect('media_video_new', '/media/video/:almanac_slug/new', controller='media', action='new_form_video', _filter=almanac_expand)
    map.connect('media_video_existing_new', '/media/video/:almanac_slug/:page_slug/new', controller='media', action='new_form_existing_video', _filter=page_expand)
    map.connect('media_video_view', '/media/video/:media_id', controller='media', action='video_view', _filter=media_expand)
    map.connect('media_video_edit', '/media/video/edit/:media_id', controller='media', action='edit_form_video', _filter=media_expand)
    map.connect('media_video_delete', '/media/video/delete/:media_id', controller='media', action='delete_video', conditions=dict(method=['POST']), _filter=media_expand)

    # add special routes to the media items themselves, so we can use nice names
    map.connect('view_media_image_large', '/media/view/image/large/:media_id/:filename', controller='media', action='view_image_large', _filter=media_expand)
    map.connect('view_media_image_small', '/media/view/image/small/:media_id/:filename', controller='media', action='view_image_small', _filter=media_expand)
    map.connect('view_media_image', '/media/view/image/:media_id/:filename', controller='media', action='view_image', _filter=media_expand)
    map.connect('view_media_audio', '/media/view/audio/:media_id/:filename', controller='media', action='view_audio', _filter=media_expand)
    map.connect('view_media_pdf', '/media/view/pdf/:media_id/:filename', controller='media', action='view_pdf', _filter=media_expand)

    return map
