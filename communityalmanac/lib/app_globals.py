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
        media_path = path.join(request.environ['pylons.pylons'].config['pylons.paths']['static_files'], 'media')
        self.images_path = config.get('images_path', path.join(media_path, 'images'))
        self.audio_path = config.get('audio_path', path.join(media_path, 'images'))
        self.pdfs_path = config.get('pdfs_path', path.join(media_path, 'images'))
