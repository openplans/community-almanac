import logging

from binascii import a2b_hex, b2a_hex
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from communityalmanac.lib.base import BaseController, render
from communityalmanac.model import Almanac
from communityalmanac.model import meta
from communityalmanac.model.meta import storage_SRID
from sqlalchemy.sql import func
from shapely import wkb
from shapely.geometry.geo import asShape
import simplejson

log = logging.getLogger(__name__)

class HomesweethomeController(BaseController):

    def home(self):
        c.almanacs = Almanac.latest()
        c.is_homepage = True
        return render('/home.mako')

    @jsonify
    def almanacs_map(self):
        json = request.params.get('extent')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        # Stupid asShape returns an Adapter instead of a Geometry.  We round
        # trip it through wkb to get the correct type.
        bbox = wkb.loads(asShape(shape).to_wkb())

        almanacs = meta.Session.query(Almanac.location).filter(func.st_intersects(Almanac.location, func.st_transform('SRID=%s;%s' % ('4326', b2a_hex(bbox.to_wkb())), storage_SRID))).limit(10).all()
        almanac_locations = [(a[0].x, a[0].y) for a in almanacs]

        return dict(almanac_locations=almanac_locations)
