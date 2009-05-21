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

"""Pylons middleware initialization"""
from beaker.middleware import CacheMiddleware, SessionMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons import config
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes.middleware import RoutesMiddleware
from os import path

from communityalmanac.config.environment import load_environment

# All sorts of repoze.who symbols.
from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.interfaces import IIdentifier
from repoze.who.interfaces import IChallenger
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.form import RedirectingFormPlugin
from repoze.who.plugins.sa import SQLAlchemyAuthenticatorPlugin
from repoze.who.plugins.sa import SQLAlchemyUserMDPlugin
from communityalmanac.model import User
from communityalmanac.model.meta import Session
from repoze.who.plugins.openid import OpenIdIdentificationPlugin


from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider
import sys

def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether this application provides a full WSGI stack (by default,
        meaning it handles its own exceptions and errors). Disable
        full_stack when this application is "managed" by another WSGI
        middleware.

    ``static_files``
        Whether this application serves its own static files; disable
        when another web server is responsible for serving them.

    ``app_conf``
        The application's local configuration. Normally specified in
        the [app:<name>] section of the Paste ini file (where <name>
        defaults to main).

    """
    # Configure the Pylons environment
    load_environment(global_conf, app_conf)

    # The Pylons WSGI app
    app = PylonsApp()

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    auth_tkt = AuthTktCookiePlugin(')h,&xCWlS}+u:<yD]BJV', 'auth_tkt')
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
    sqlauth = SQLAlchemyAuthenticatorPlugin(User, Session)
    sqlauth.translations['user_name'] = 'username'
    sqlauth.translations['validate_password'] = 'authenticate'

    sqlmetadata = SQLAlchemyUserMDPlugin(User, Session)
    sqlmetadata.translations['user_name'] = 'username'

    identifiers = [('form', formplugin), ('openid', openid),('auth_tkt',auth_tkt)]
    authenticators = [('sqlauth', sqlauth), ('openid', openid)]
    challengers = [('form', formplugin), ('openid', openid)]
    mdproviders = [('sqlmetadata', sqlmetadata)]
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

    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])

    # Establish the Registry for this application
    app = RegistryManager(app)

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        app = Cascade([static_app, app])

    return app
