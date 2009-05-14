import logging

from pylons import request, response, session, tmpl_context as c
from pylons import g
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
from pylons.decorators import jsonify

log = logging.getLogger(__name__)

class GeocoderController(BaseController):

    @jsonify
    def geocode(self):
        location = request.GET.get('location')
        if location is None:
            abort(400)
        from geopy import geocoders
        geoc = geocoders.Google(g.map_key)
        try:
            place, (lat, lng) = geoc.geocode(location)
        except ValueError:
            return {}
        else:
            return dict(lat=lat, lng=lng)
