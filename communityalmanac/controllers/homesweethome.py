import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from communityalmanac.lib.base import BaseController, render
from communityalmanac.model import Almanac
from communityalmanac.model import meta
from sqlalchemy.sql import func

log = logging.getLogger(__name__)

class HomesweethomeController(BaseController):

    def home(self):
        c.almanacs = Almanac.latest()
        c.is_homepage = True
        return render('/home.mako')

    @jsonify
    def almanacs_map(self,):

        json = request.params.get('extent')
        if json is None:
            abort(400)
        shape = simplejson.loads(json)
        # Stupid asShape returns an Adapter instead of a Geometry.  We round
        # trip it through wkb to get the correct type.
        bbox = wkb.loads(asShape(shape).to_wkb())

        almanacs = meta.Session.query(Almanac).filter(func.st_intersects(Almanac.location,bbox)).limit(10)

        return dict(html=render('/media/map/item.mako'),
                    map_id='pagemedia_%d' % map.id,
                    geometry=json,
                    )
