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
from shapely.geometry.point import Point
import simplejson

class GeocoderController(BaseController):

    @jsonify
    def geocode(self):
        location = request.GET.get('location')
        if location is None:
            abort(400)
        geoc = geocoders.Google(g.map_key, output_format='json')
        try:
            result = GeocoderController._result_with_locality(geoc.geocode(location, exactly_one=False))
            if not result:
                return {}
            if not result.locality or not result.administrative:
                result = GeocoderController._result_with_locality(geoc.geocode('%f, %f' % (result.latitude, result.longitude), exactly_one=False))
            place, (lat, lng) = result
        except ValueError:
            return {}
        if result.locality and result.administrative:
            authoritative_name = '%s, %s' % (result.locality, result.administrative)
        else:
            authoritative_name = None
        try:
            meta.Session.query(Almanac).filter(Almanac.name==authoritative_name).one()
            almanac = True
        except exc.NoResultFound:
            almanac = False
        geopoint = Point(lat, lng)
        return dict(lat=lat, lng=lng, geojson=simplejson.dumps(geopoint.__geo_interface__), authoritative_name=authoritative_name, almanac=almanac)

    @staticmethod
    def _result_with_locality(gen):
        first = None
        for x in gen:
            if not first:
                first = x
            if x and x.locality and x.administrative:
                return x
        return first
