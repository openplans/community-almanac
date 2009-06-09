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

from pylons import request, response, session, tmpl_context as c, g
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
from communityalmanac.model import Audio
from communityalmanac.model import Image
from communityalmanac.model import Map
from communityalmanac.model import PDF
from communityalmanac.model import Story
from communityalmanac.model import meta
from pylons.decorators import jsonify
from pylons.decorators.rest import dispatch_on
from shapely import wkb
from shapely.geometry.geo import asShape
import communityalmanac.lib.helpers as h
import os
import uuid
import simplejson

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
        if not h.sort_media_items(id, index):
            abort(400)
        # The only useful return value is the HTTP response, so we return an
        # empty body.
        return ''

    def donothing(self, almanac_slug):
        abort(400)

    @dispatch_on(POST='_do_new_form_text')
    @jsonify
    def new_form_text(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        c.legend = u'Text'
        return dict(html=render('/media/story/form.mako'))

    @jsonify
    def _do_new_form_text(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        body = request.POST.get('body', u'')
        if not body:
            abort(400)

        page = c.almanac.new_page(self.ensure_user)

        c.story = story = Story()
        story.text = body
        story.page_id = page.id
        story.order = len(page.media)
        meta.Session.add(story)
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/story/item.mako'))

    @dispatch_on(POST='_do_new_form_existing_text')
    @jsonify
    def new_form_existing_text(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.legend = u'Text'
        return dict(html=render('/media/story/form.mako'))

    @jsonify
    def _do_new_form_existing_text(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = page = h.get_page_by_slug(c.almanac, page_slug)
        body = request.POST.get('body', u'')
        if not body:
            abort(400)

        c.story = story = Story()
        story.text = body
        story.page_id = page.id
        story.order = len(page.media)
        meta.Session.add(story)
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/story/item.mako'))

    @dispatch_on(POST='_do_edit_form_text')
    @jsonify
    def edit_form_text(self, media_id):
        c.media_item = h.get_media_by_id(media_id)
        c.view_url = h.url_for('media_story_view', media_id=c.media_item.id)
        c.legend = u'Text'
        return dict(html=render('/media/story/form.mako'))

    @jsonify
    def _do_edit_form_text(self, media_id):
        c.story = h.get_media_by_id(media_id)
        body = request.POST.get('body', u'')
        if not body:
            abort(400)

        c.story.text = body
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/story/item.mako'))

    @jsonify
    def text_view(self, media_id):
        c.editable = True
        c.story = h.get_media_by_id(media_id)
        return dict(html=render('/media/story/item.mako'))

    @jsonify
    def delete_text(self, media_id):
        story = h.get_media_by_id(media_id)
        meta.Session.delete(story)
        meta.Session.commit()

    @dispatch_on(POST='_do_new_form_map')
    @jsonify
    def new_form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        loc = c.almanac.location
        c.map_id = str(uuid.uuid4())
        c.legend = u'Map'
        return dict(html=render('/media/map/form.mako'),
                    lat=loc.x, lng=loc.y,
                    map_id=c.map_id,
                    )

    @jsonify
    def _do_new_form_map(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        json = request.POST.get('feature')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        # Stupid asShape returns a PointAdapter instead of a Point.  We round
        # trip it through wkb to get the correct type.
        location = wkb.loads(asShape(shape).to_wkb())

        c.map = map = Map()
        map.location = location
        map.page_id = page.id
        map.order = len(page.media)
        meta.Session.add(map)
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/map/item.mako'),
                    map_id='pagemedia_%d' % map.id,
                    geometry=json,
                    )

    @dispatch_on(POST='_do_new_form_existing_map')
    @jsonify
    def new_form_existing_map(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        loc = c.almanac.location
        c.map_id = str(uuid.uuid4())
        c.legend = u'Map'
        return dict(html=render('/media/map/form.mako'),
                    lat=loc.x, lng=loc.y,
                    map_id=c.map_id,
                    )

    @jsonify
    def _do_new_form_existing_map(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = page = h.get_page_by_slug(c.almanac, page_slug)
        json = request.POST.get('feature')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        # Stupid asShape returns a PointAdapter instead of a Point.  We round
        # trip it through wkb to get the correct type.
        location = wkb.loads(asShape(shape).to_wkb())

        c.map = map = Map()
        map.location = location
        map.page_id = page.id
        map.order = len(page.media)
        meta.Session.add(map)
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/map/item.mako'),
                    map_id='pagemedia_%d' % map.id,
                    geometry=json,
                    )

    @dispatch_on(POST='_do_edit_form_map')
    @jsonify
    def edit_form_map(self, media_id):
        c.media_item = c.map = h.get_media_by_id(media_id)
        geometry = c.map.location.__geo_interface__
        geojson = simplejson.dumps(geometry)
        c.view_url = h.url_for('media_map_view', media_id=c.media_item.id)
        c.legend = u'Map'
        return dict(html=render('/media/map/form.mako'),
                    map_id='pagemedia_%d' % c.map.id,
                    geometry=geojson,
                    )

    @jsonify
    def _do_edit_form_map(self, media_id):
        c.map = h.get_media_by_id(media_id)
        json = request.POST.get('feature')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        # Stupid asShape returns a PointAdapter instead of a Point.  We round
        # trip it through wkb to get the correct type.
        location = wkb.loads(asShape(shape).to_wkb())

        c.map.location = location
        meta.Session.commit()

        c.editable = True
        return dict(html=render('/media/map/item.mako'),
                    map_id='pagemedia_%d' % c.map.order,
                    geometry=json,
                    )

    @jsonify
    def map_view(self, media_id):
        c.editable = True
        c.map = h.get_media_by_id(media_id)
        geometry = c.map.location.__geo_interface__
        geojson = simplejson.dumps(geometry)
        return dict(html=render('/media/map/item.mako'),
                    map_id='pagemedia_%d' % c.map.id,
                    geometry=geojson,
                    )

    @jsonify
    def delete_map(self, media_id):
        map = h.get_media_by_id(media_id)
        meta.Session.delete(map)
        meta.Session.commit()

    @dispatch_on(POST='_do_new_form_image')
    @jsonify
    def new_form_image(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.legend = u'Image'
        return dict(html=render('/media/image/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    #@jsonify
    #XXX ajax file upload plugin does not like response type of
    # application/json
    def _do_new_form_image(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        image_file = request.POST.get('userfile')
        if image_file is None:
            abort(400)

        page = c.almanac.new_page(self.ensure_user)

        image_file.make_file()
        image_data = image_file.file.read()
        new_uuid = str(uuid.uuid4())
        path = os.path.join(g.images_path, new_uuid)
        f = open(path, 'w')
        f.write(image_data)
        f.close()

        c.image = image = Image()
        image.path = path
        image.page_id = page.id
        image.order = len(page.media)
        meta.Session.add(image)
        meta.Session.commit()

        c.editable = True

        # Our output is being consumed in an iframe.  (Necessary in order to
        # simulate an AJAX file upload.)  This means that our response is going
        # to be mangled by the browser no matter what we do.  There are two
        # possible solutions to this.
        #
        # The first is to send the content as 'application/javascript' or
        # 'text/javascript', but then the iframe will return a non-existant
        # <pre> tag surrounding the content.  The client side javascript must
        # be aware of this and strip the tag.
        #
        # The second is to send the content as text/html, and make sure that we
        # don't send any angle brackets that the browser might interpret as
        # HTML.  In the case of a JSON response, angle brackets are only valid
        # inside of a string, and so a simple search and replace which puts in
        # their hex encodings is sufficient to protect the content.
        # e.g. return json_output.replace('<','\\x3C').replace('>','\\x3E')
        #
        # I've fixed the external library to support the first option,
        # hopefully the patch will be accepted.  In the meantime, our embedded
        # version works properly, and the client-side fix ensures that we only
        # have to write the code once, rather than every time we use the file
        # uploader*
        #
        # * Not exactly true, since you can't use @jsonify, but it's a close as
        # we can get.

        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/image/item.mako')))

    @dispatch_on(POST='_do_new_form_existing_image')
    @jsonify
    def new_form_existing_image(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.legend = u'Image'
        return dict(html=render('/media/image/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_new_form_existing_image(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = page = h.get_page_by_slug(c.almanac, page_slug)
        image_file = request.POST.get('userfile')
        if image_file is None:
            abort(400)

        image_file.make_file()
        image_data = image_file.file.read()
        new_uuid = str(uuid.uuid4())
        path = os.path.join(g.images_path, new_uuid)
        f = open(path, 'w')
        f.write(image_data)
        f.close()

        c.image = image = Image()
        image.path = path
        image.page_id = page.id
        image.order = len(page.media)
        meta.Session.add(image)
        meta.Session.commit()

        c.editable = True
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/image/item.mako')))

    @dispatch_on(POST='_do_edit_form_image')
    @jsonify
    def edit_form_image(self, media_id):
        c.media_item = c.image = h.get_media_by_id(media_id)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.view_url = h.url_for('media_image_view', media_id=c.media_item.id)
        c.legend = u'Image'
        return dict(html=render('/media/image/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_edit_form_image(self, media_id):
        c.image = h.get_media_by_id(media_id)
        image_file = request.POST.get('userfile')
        if image_file is None:
            abort(400)

        image_file.make_file()
        image_data = image_file.file.read()
        f = open(c.image.path, 'w')
        f.write(image_data)
        f.close()

        meta.Session.commit()

        c.editable = True
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/image/item.mako')))

    @jsonify
    def image_view(self, media_id):
        c.editable = True
        c.image = h.get_media_by_id(media_id)
        return dict(html=render('/media/image/item.mako'))

    @jsonify
    def delete_image(self, media_id):
        image = h.get_media_by_id(media_id)
        os.unlink(image.path)
        meta.Session.delete(image)
        meta.Session.commit()

    @dispatch_on(POST='_do_new_form_pdf')
    @jsonify
    def new_form_pdf(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.legend = u'PDF'
        return dict(html=render('/media/pdf/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_new_form_pdf(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        pdf_file = request.POST.get('userfile')
        if pdf_file is None:
            abort(400)

        page = c.almanac.new_page(self.ensure_user)

        pdf_file.make_file()
        pdf_data = pdf_file.file.read()
        new_uuid = str(uuid.uuid4())
        path = os.path.join(g.pdfs_path, new_uuid)
        f = open(path, 'w')
        f.write(pdf_data)
        f.close()

        c.pdf = pdf = PDF()
        pdf.path = path
        pdf.page_id = page.id
        pdf.order = len(page.media)
        meta.Session.add(pdf)
        meta.Session.commit()

        c.editable = True
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/pdf/item.mako')))

    @dispatch_on(POST='_do_new_form_existing_pdf')
    @jsonify
    def new_form_existing_pdf(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.legend = u'pdf'
        return dict(html=render('/media/pdf/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_new_form_existing_pdf(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = page = h.get_page_by_slug(c.almanac, page_slug)
        pdf_file = request.POST.get('userfile')
        if pdf_file is None:
            abort(400)

        pdf_file.make_file()
        pdf_data = pdf_file.file.read()
        new_uuid = str(uuid.uuid4())
        path = os.path.join(g.pdfs_path, new_uuid)
        f = open(path, 'w')
        f.write(pdf_data)
        f.close()

        c.pdf = pdf = PDF()
        pdf.path = path
        pdf.page_id = page.id
        pdf.order = len(page.media)
        meta.Session.add(pdf)
        meta.Session.commit()

        c.editable = True
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/pdf/item.mako')))

    @dispatch_on(POST='_do_edit_form_pdf')
    @jsonify
    def edit_form_pdf(self, media_id):
        c.media_item = c.pdf = h.get_media_by_id(media_id)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.view_url = h.url_for('media_pdf_view', media_id=c.media_item.id)
        c.legend = u'PDF'
        return dict(html=render('/media/pdf/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_edit_form_pdf(self, media_id):
        c.pdf = h.get_media_by_id(media_id)
        pdf_file = request.POST.get('userfile')
        if pdf_file is None:
            abort(400)

        pdf_file.make_file()
        pdf_data = pdf_file.file.read()
        f = open(c.pdf.path, 'w')
        f.write(pdf_data)
        f.close()

        meta.Session.commit()

        c.editable = True
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/pdf/item.mako')))

    @jsonify
    def pdf_view(self, media_id):
        c.editable = True
        c.pdf = h.get_media_by_id(media_id)
        return dict(html=render('/media/pdf/item.mako'))

    @jsonify
    def delete_pdf(self, media_id):
        pdf = h.get_media_by_id(media_id)
        os.unlink(pdf.path)
        meta.Session.delete(pdf)
        meta.Session.commit()

    @dispatch_on(POST='_do_new_form_audio')
    @jsonify
    def new_form_audio(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        page = c.almanac.new_page(self.ensure_user)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.legend = u'audio'
        return dict(html=render('/media/audio/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_new_form_audio(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        audio_file = request.POST.get('userfile')
        if audio_file is None:
            abort(400)

        page = c.almanac.new_page(self.ensure_user)

        audio_file.make_file()
        audio_data = audio_file.file.read()
        new_uuid = str(uuid.uuid4())
        fname = '%s.mp3' % new_uuid
        path = os.path.join(g.audio_path, fname)
        f = open(path, 'w')
        f.write(audio_data)
        f.close()

        c.audio = audio = Audio()
        audio.path = path
        audio.page_id = page.id
        audio.order = len(page.media)
        meta.Session.add(audio)
        meta.Session.commit()

        c.editable = True
        c.flowplayer_id = new_uuid
        c.audio_url = request.application_url + c.audio.url
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/audio/item.mako')))

    @dispatch_on(POST='_do_new_form_existing_audio')
    @jsonify
    def new_form_existing_audio(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = h.get_page_by_slug(c.almanac, page_slug)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.legend = u'audio'
        return dict(html=render('/media/audio/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_new_form_existing_audio(self, almanac_slug, page_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        c.page = page = h.get_page_by_slug(c.almanac, page_slug)
        audio_file = request.POST.get('userfile')
        if audio_file is None:
            abort(400)

        audio_file.make_file()
        audio_data = audio_file.file.read()
        new_uuid = str(uuid.uuid4())
        fname = '%s.mp3' % new_uuid
        path = os.path.join(g.audio_path, fname)
        f = open(path, 'w')
        f.write(audio_data)
        f.close()

        c.audio = audio = Audio()
        audio.path = path
        audio.page_id = page.id
        audio.order = len(page.media)
        meta.Session.add(audio)
        meta.Session.commit()

        c.editable = True
        c.flowplayer_id = new_uuid
        c.audio_url = request.application_url + c.audio.url
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/audio/item.mako')))

    @dispatch_on(POST='_do_edit_form_audio')
    @jsonify
    def edit_form_audio(self, media_id):
        c.media_item = c.audio = h.get_media_by_id(media_id)
        c.file_id = str(uuid.uuid4())
        c.file_upload_url = request.path_url
        c.flowplayer_id = str(uuid.uuid4())
        c.audio_url = request.application_url + c.audio.url
        c.view_url = h.url_for('media_audio_view', media_id=c.media_item.id)
        c.legend = u'audio'
        return dict(html=render('/media/audio/form.mako'),
                    file_id=c.file_id,
                    file_upload_url=c.file_upload_url,
                    )

    def _do_edit_form_audio(self, media_id):
        c.audio = h.get_media_by_id(media_id)
        audio_file = request.POST.get('userfile')
        if audio_file is None:
            abort(400)

        audio_file.make_file()
        audio_data = audio_file.file.read()
        f = open(c.audio.path, 'w')
        f.write(audio_data)
        f.close()

        meta.Session.commit()

        c.editable = True
        c.flowplayer_id = str(uuid.uuid4())
        c.audio_url = request.application_url + c.audio.url
        response.content_type = 'application/javascript'
        return simplejson.dumps(dict(html=render('/media/audio/item.mako')))

    @jsonify
    def audio_view(self, media_id):
        c.editable = True
        c.audio = h.get_media_by_id(media_id)
        c.flowplayer_id = str(uuid.uuid4())
        c.audio_url = request.application_url + c.audio.url
        return dict(html=render('/media/audio/item.mako'))

    @jsonify
    def delete_audio(self, media_id):
        audio = h.get_media_by_id(media_id)
        os.unlink(audio.path)
        meta.Session.delete(audio)
        meta.Session.commit()
