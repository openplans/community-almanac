# -*- mode: python; -*-

import os, sys, site

BASE='/var/www/communityalmanac.org'
SP = BASE + '/current/lib/python2.6/site-packages'
EC = BASE + '/python-egg-cache'
CONF = BASE + '/production.ini'

for f in (BASE, SP, EC, CONF):
    assert os.path.exists(f), "%s does not exist" % f

site.addsitedir(BASE + SP)
os.environ['PYTHON_EGG_CACHE'] = BASE + EC

from paste.deploy import loadapp

application = loadapp('config:%s' % CONF)
