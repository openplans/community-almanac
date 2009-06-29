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

from repoze.what.plugins.sql import configure_sql_adapters
from repoze.what.middleware import setup_auth as setup_authorization
from repoze.what.middleware import AuthorizationMetadata

# All sorts of repoze.who symbols.
from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.interfaces import IIdentifier
from repoze.who.interfaces import IChallenger
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.form import RedirectingFormPlugin
from repoze.who.plugins.sa import SQLAlchemyAuthenticatorPlugin
from repoze.who.plugins.sa import SQLAlchemyUserMDPlugin
from repoze.who.plugins.openid import OpenIdIdentificationPlugin


from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider
from repoze.what.predicates import Predicate
from communityalmanac.model import FullUser
from communityalmanac.model.meta import Session
from communityalmanac.model import meta, User, Group, Permission
import communityalmanac.lib.helpers as h
from pylons import config
from pylons import session
from pylons import tmpl_context as c

from os import path
import sys

class is_media_owner(Predicate):
    """
    Check that the current user owns the media in question.

    Example::

        p = is_media_owner()

    """
    message = u'The user must have the own this media'

    def __init__(self, **kwargs):
        super(is_media_owner, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):

        user = c.user
        if not user:
            userid = session.setdefault('userid', None)
            if not userid:
                self.unmet()
            user = meta.Session.query(User).get(userid)
            if not user:
                self.unmet()

        media_id = environ['pylons.routes_dict']['media_id']
        media = h.get_media_by_id(media_id)

        if media.page.user_id == user.id:
            return
        if credentials and \
           'manage' in credentials.get('permissions'):
            return
        self.unmet()

class is_page_owner(Predicate):
    """
    Check that the current user owns the page in question.

    Example::

        p = is_page_owner()

    """
    message = u'The user must have the own this page'

    def __init__(self, **kwargs):
        super(is_page_owner, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):

        user = c.user
        if not user:
            userid = session.setdefault('userid', None)
            if not userid:
                self.unmet()
            user = meta.Session.query(User).get(userid)
            if not user:
                self.unmet()

        almanac_slug = environ['pylons.routes_dict']['almanac_slug']
        page_slug = environ['pylons.routes_dict']['page_slug']

        almanac = h.get_almanac_by_slug(almanac_slug)
        page = h.get_page_by_slug(almanac, page_slug)

        if page.user_id == user.id:
            return
        if credentials and \
           'manage' in credentials.get('permissions'):
            return
        self.unmet()

def valid_user(username):
    return meta.Session.query(FullUser).filter(FullUser.username==username).count() == 1

def wsgi_authorization(app, app_conf):
    """Add a WSGI middleware wrapper to this application."""
    source_adapters = configure_sql_adapters(
        FullUser,
        Group,
        Permission,
        meta.Session,
        dict(section_name='name', item_name='username'),
        dict(section_name='name', item_name='name')
        )
    group_adapters = {'sql_auth': source_adapters['group']}
    permission_adapters = {'sql_auth': source_adapters['permission']}

    auth_tkt = AuthTktCookiePlugin(')h,&xCWlS}+u:<yD]BJV', 'auth_tkt', userid_checker=valid_user)
    openid = OpenIdIdentificationPlugin('file', # 'mem'
            openid_field = 'openid',
            error_field = 'error',
            session_name = 'beaker.session',
            login_form_url = '/login_form',
            login_handler_path = '/_do_login',
            logout_handler_path = '/logout',
            store_file_path = path.join(config['pylons.cache_dir'], 'sstore'),
            logged_in_url = '/success',
            logged_out_url = '/',
            came_from_field = 'came_from',
            rememberer_name = 'auth_tkt',
            sql_associations_table = '',
            sql_nonces_table = '',
            sql_connstring = ''
            )

    formplugin = RedirectingFormPlugin('/login', '/do_login', '/logout', rememberer_name='auth_tkt')
    sqlauth = SQLAlchemyAuthenticatorPlugin(FullUser, Session)
    sqlauth.translations['user_name'] = 'username'
    sqlauth.translations['validate_password'] = 'authenticate'

    sqlmetadata = SQLAlchemyUserMDPlugin(FullUser, Session)
    sqlmetadata.translations['user_name'] = 'username'
    authorization = AuthorizationMetadata(group_adapters,
                                          permission_adapters)

    identifiers = [('form', formplugin), ('openid', openid),('auth_tkt',auth_tkt)]
    authenticators = [('sqlauth', sqlauth), ('openid', openid)]
    challengers = [('form', formplugin), ('openid', openid)]
    mdproviders = [('sqlmetadata', sqlmetadata), ('authorization_md', authorization)]
    log_stream = None
    #if config.get('WHO_LOG'):
    log_stream = sys.stdout

    app = PluggableAuthenticationMiddleware(
        app,
        identifiers,
        authenticators,
        challengers,
        mdproviders,
        default_request_classifier,
        default_challenge_decider,
        log_stream = log_stream,
        log_level=app_conf.get('who.log_level','error')
        )
    return app
