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

"""Setup the communityalmanac application"""
from __future__ import with_statement
import logging

from communityalmanac.config.environment import load_environment
from communityalmanac.model import meta, FullUser, Group, Permission
from random import sample
from string import letters, digits, punctuation

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup communityalmanac here"""
    load_environment(conf.global_conf, conf.local_conf)

    if meta.engine.name == 'sqlite':
        from communityalmanac.lib.spatialite import SQLITE_INIT
        with open(SQLITE_INIT) as initscript:
            conn = meta.engine.connect()
            for line in initscript.readlines():
                conn.execute(line)

        # Create the tables if they don't already exist
        meta.metadata.create_all(bind=meta.engine,checkfirst=False)
    else:

        # Create the tables if they don't already exist
        meta.metadata.create_all(bind=meta.engine)

    # Create the admin group and permission, and generate an admin user...
    managers = Group(name='managers')
    meta.Session.add(managers)

    can_manage = Permission(name='manage')
    meta.Session.add(can_manage)

    managers.permissions.append(can_manage)

    admin = FullUser(username='admin')
    password = ''.join(sample(letters + digits + punctuation, 20))
    admin.set_password(password)
    meta.Session.add(admin)

    admin.groups.append(managers)

    meta.Session.commit()
    print "Creating initial admin account:\nUsername: %s\nPassword: %s" % (admin.username, password)

