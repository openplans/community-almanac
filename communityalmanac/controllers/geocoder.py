import logging

from pylons import request, response, session, tmpl_context as c
from pylons import g
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
from pylons.decorators import jsonify

log = logging.getLogger(__name__)

from geopy import geocoders
from communityalmanac.model import meta, Almanac
from sqlalchemy.orm import exc

class GeocoderController(BaseController):

    @jsonify
    def geocode(self):
        location = request.GET.get('location')
        if location is None:
            abort(400)
        geoc = geocoders.Google(g.map_key, output_format='json')
        try:
            result = GeocoderController._get_first(geoc.geocode(location, exactly_one=False))
            if not result.locality:
                result = GeocoderController._get_first(geoc.geocode('%f, %f' % (result.latitude, result.longitude), exactly_one=False))
            place, (lat, lng) = result
        except ValueError:
            return {}
        authoritative_name = '%s, %s' % (result.locality, result.administrative)
        try:
            almanac_slug = meta.Session.query(Almanac).filter(Almanac.name==authoritative_name).one().slug
        except exc.NoResultFound:
            almanac_slug = ''
        return dict(lat=lat, lng=lng, authoritative_name=authoritative_name, almanac_slug=almanac_slug)

    @staticmethod
    def _get_first(gen):
        for x in gen:
            return x
