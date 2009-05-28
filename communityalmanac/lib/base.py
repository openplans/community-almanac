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
from __future__ import with_statement
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import session

from communityalmanac.model import AnonymousUser
from communityalmanac.model import User
from communityalmanac.model import meta
from pylons.controllers.util import redirect_to
from pylons import request, tmpl_context as c
from os import path
import re
STYLE_URL = re.compile(r"""url\("(.*?)"\)|url\('(.*?)'\)|url\((.*?)\)""")

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

    def __before__(self):
        identity = request.environ.get('repoze.who.identity')
        if identity:
            c.user = identity['user']
        else:
            c.user = None

    @property
    def ensure_user(self):
        if c.user:
            return c.user
        # Check for session user
        userid = session.setdefault('userid', None)
        if userid:
            return meta.Session.query(User).get(userid)
        user = AnonymousUser()
        meta.Session.add(user)
        meta.Session.commit()
        session['userid'] = user.id
        session.save()

    def _email_strip(self, html, message):
        # Todo, strip extra white space...
        import lxml.html
        doc = lxml.html.fromstring(html)

        # Remove all POST forms (since you typically can't post from email)
        for form in doc.cssselect('form'):
            form.getparent().remove(form)

        # Remove the javascript
        for script in doc.cssselect('script'):
            script.getparent().remove(script)

        if not hasattr(self, '_embedded_images'):
            self._embedded_images = {}

        # Embed images
        for image in doc.cssselect('img'):
            location = image.attrib['src']
            # We pull the static files directory from pylons setup configuration
            public = request.environ['pylons.pylons'].config['pylons.paths']['static_files']
            filepath = path.abspath(path.join(public, './%s' % location))
            filename = path.basename(filepath)
            if filepath not in self._embedded_images:
                self._embedded_images[filepath] = filename
                message.attach(filepath, filename)
            image.attrib['src'] = 'cid:%s' % filename

        # Fixup background attribute images
        for element in doc.cssselect('*[background]'):
            location = element.attrib['background']
            # We pull the static files directory from pylons setup configuration
            public = request.environ['pylons.pylons'].config['pylons.paths']['static_files']
            filepath = path.abspath(path.join(public, './%s' % location))
            filename = path.basename(filepath)
            if filepath not in self._embedded_images:
                self._embedded_images[filepath] = filename
                message.attach(filepath, filename)
            element.attrib['background'] = 'cid:%s' % filename

        #embed stylesheets
        for stylesheet in doc.cssselect('link[rel=stylesheet]'):
            head = stylesheet.getparent()
            location = stylesheet.attrib['href']
            # We pull the static files directory from pylons setup configuration
            public = request.environ['pylons.pylons'].config['pylons.paths']['static_files']
            filepath = path.abspath(path.join(public, './%s' % location))
            try:
                with open(path.abspath(filepath)) as stylefile:
                    styledata = stylefile.read()
            except:
                continue

            styledata = self._style_fixup(styledata, message)
            head.remove(stylesheet)
            head.append(lxml.html.fromstring("""<style type="text/css" media="screen">%s</style>""" % styledata))

        # Fixup embedded styles
        for element in doc.iter():
            if 'style' in element.attrib:
                element.attrib['style'] = self._style_fixup(element.attrib['style'], message)

        # We need to take the text content from the body
        body = doc.cssselect('body')[0]
        text_content = body.text_content().encode('utf8')
        return text_content, lxml.html.tostring(doc).encode('utf8')

    def _style_fixup(self, styledata, message):
        if not hasattr(self, '_embedded_images'):
            self._embedded_images = {}
        def image_embed(matchobj):
            filepath = path.abspath(path.join(__file__, '../../public', './%s' % (matchobj.group(1) or matchobj.group(2) or matchobj.group(3))))
            try:
                with open(path.abspath(filepath)) as stylefile:
                    pass
            except:
                return matchobj.group(0)
            filename = path.basename(filepath)
            if filepath not in self._embedded_images:
                self._embedded_images[filepath] = filename
                message.attach(filepath, filename)
            return "url(cid:%s)" % filename
        return re.sub(STYLE_URL, image_embed, styledata)

