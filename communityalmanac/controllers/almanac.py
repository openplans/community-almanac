import logging

from communityalmanac.lib.helpers import name_almanac
from communityalmanac.model import Almanac
from communityalmanac.model import meta
from formencode import Invalid
from formencode import Schema
from formencode import validators
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
from sqlalchemy.orm import exc
import communityalmanac.lib.helpers as h

from communityalmanac.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AlmanacCreateForm(Schema):
    name = validators.String(not_empty=True)

class AlmanacController(BaseController):

    def home(self):
        c.almanacs = Almanac.latest()
        return render('/home.mako')

    @dispatch_on(POST='_do_create')
    def create(self):
        return render('/almanac/create.mako')

    @validate(schema=AlmanacCreateForm(), form='create')
    def _do_create(self):
        name = self.form_result['name']
        slug = name_almanac(name)
        almanac = Almanac(name, slug)

        meta.Session.save(almanac)
        meta.Session.commit()

        redirect_to(h.url_for('almanac_view', almanac_slug=slug))

    def view(self, almanac_slug):
        c.almanac = h.get_almanac_by_slug(almanac_slug)
        return render('/almanac/view.mako')
