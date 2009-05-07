import logging

from communityalmanac.model import Almanac
from communityalmanac.model import meta
from formencode import Invalid
from formencode import Schema
from formencode import validators
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
import communityalmanac.lib.helpers as h

from communityalmanac.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AlmanacCreateForm(Schema):
    name = validators.String(not_empty=True)

class AlmanacController(BaseController):

    def home(self):
        return render('/home.mako')

    @dispatch_on(POST='_do_create')
    def create(self):
        return render('/almanac/create.mako')

    @validate(schema=AlmanacCreateForm(), form='create')
    def _do_create(self):
        name = self.form_result['name']
        from communityalmanac.lib.helpers import name_almanac
        name = name_almanac(name)
        almanac = Almanac(name)
        
        # FIXME should we fire some sort of event here? would be useful for logging purposes
        meta.Session.save(almanac)
        meta.Session.commit()

        # FIXME work out the slug story
        redirect_to(h.url_for('almanac_view', almanac_slug=name))

    def view(self, almanac_slug):
        return u'Now viewing an almanac with slug: %s' % almanac_slug
