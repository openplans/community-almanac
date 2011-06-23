# -*- mode: python; -*-

import os, sys, site

# Work around libraries polluting stdout. see
# https://code.google.com/p/modwsgi/wiki/ApplicationIssues
sys.stdout = sys.stderr

BASE='/var/www/communityalmanac.org'
SP = BASE + '/current/lib/python2.6/site-packages'
EC = BASE + '/python-egg-cache'
CONF = BASE + '/production.ini'

for f in (BASE, SP, EC, CONF):
    assert os.path.exists(f), "%s does not exist" % f

site.addsitedir(BASE + SP)
os.environ['PYTHON_EGG_CACHE'] = BASE + EC

from paste.deploy import loadapp

# Need this for logging under mod_wsgi.
# See https://groups.google.com/group/pylons-discuss/browse_thread/thread/9b9add4529b3779c
# ... if this is documented anywhere other than that thread, it sure is obscure
from paste.script.util.logging_config import fileConfig
fileConfig(CONF)

application = loadapp('config:%s' % CONF)
