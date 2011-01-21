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

"""The application's Globals object"""
from paste.deploy.converters import asbool
from paste.deploy.converters import aslist
from pylons import config, request
from os import path

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.map_key = config['map_key']

        self.captcha_enabled = asbool(config['captcha_enabled'])
        self.captcha_pubkey = config['captcha_pubkey']
        self.captcha_privkey = config['captcha_privkey']

        self.akismet_enabled = asbool(config['akismet_enabled'])
        self.akismet_key = config['akismet_key']
        self.akismet_url = config['akismet_url']

        self.allow_tags = aslist(config['allow_tags'], sep=',')
        host_whitelist = aslist(config['host_whitelist'], sep=',')
        # prefix www subdomain to all hosts as a convenience
        self.host_whitelist = set(host_whitelist)
        for host in host_whitelist:
            if not host.startswith('www.'):
                self.host_whitelist.add('www.' + host)

        self.support_sending_enabled = asbool(config['support_sending_enabled'])
        self.support_email = config['support_email']
        self.smtp_host = config['smtp_server']
        self.smtp_port = config['smtp_port']

    @property
    def images_path(self):
        media_path = path.join(request.environ['pylons.pylons'].config['pylons.paths']['static_files'], 'media')
        return config.get('images_path', path.join(media_path, 'images'))

    @property
    def audio_path(self):
        media_path = path.join(request.environ['pylons.pylons'].config['pylons.paths']['static_files'], 'media')
        return config.get('audio_path', path.join(media_path, 'images'))

    @property
    def pdfs_path(self):
        media_path = path.join(request.environ['pylons.pylons'].config['pylons.paths']['static_files'], 'media')
        return config.get('pdfs_path', path.join(media_path, 'images'))
