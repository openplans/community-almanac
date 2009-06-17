import logging

from binascii import a2b_hex, b2a_hex
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from communityalmanac.lib.base import BaseController, render
from communityalmanac.model import Almanac
from communityalmanac.model import Page
from communityalmanac.model import meta
from communityalmanac.model.meta import storage_SRID
from sqlalchemy.sql import func
from shapely import wkb
from shapely.geometry.geo import asShape
import simplejson

log = logging.getLogger(__name__)

class HomesweethomeController(BaseController):

    def home(self):
        c.limit, c.offset = int(request.params.get('limit', 10)), int(request.params.get('offset', 0))
        c.almanacs = Almanac.latest(c.limit, c.offset)
        c.pages = Page.latest(c.limit, c.offset)
        c.n_almanacs = Almanac.n_almanacs()
        c.is_homepage = True
        return render('/home.mako')

    def almanacs_kml(self):
        json = request.params.get('extent')
        if json is None:
            # We need to make sure we only select almanacs with pages here...
            c.almanacs = meta.Session.query(Almanac).join(Almanac.pages).distinct().limit(10).all()
        else:
            shape = simplejson.loads(json)
            # Stupid asShape returns an Adapter instead of a Geometry.  We round
            # trip it through wkb to get the correct type.
            bbox = wkb.loads(asShape(shape).to_wkb())

            c.almanacs = meta.Session.query(Almanac).join(Almanac.pages).distinct().filter(func.st_intersects(Almanac.location, func.st_transform('SRID=%s;%s' % ('4326', b2a_hex(bbox.to_wkb())), storage_SRID))).limit(10).all()
        return render('/almanac/kml.mako')
