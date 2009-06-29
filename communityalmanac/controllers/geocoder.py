import logging

from pylons import request, response, session, tmpl_context as c
from pylons import g
from pylons.controllers.util import abort, redirect_to

from communityalmanac.lib.base import BaseController, render
from pylons.decorators import jsonify

log = logging.getLogger(__name__)

from geopy import geocoders
from communityalmanac.model import meta, Almanac
from communityalmanac.model.meta import storage_SRID
from binascii import a2b_hex, b2a_hex
from sqlalchemy.orm import exc
from sqlalchemy.sql import func
from shapely.geometry.point import Point
from shapely.geometry.geo import asShape
import simplejson

class GeocoderController(BaseController):

    @jsonify
    def geocode(self):
        # The geocoder works from either a name or a point.
        location = request.GET.get('location')
        bbox = simplejson.loads(request.GET.get('bbox','false'))
        if location is None and not bbox:
            abort(400)

        geoc = geocoders.Google(g.map_key, output_format='json')

        name_based = False
        if not bbox:
            # We don't have a point, so we work with the name...
            name_based = True
            try:
                result = GeocoderController._result_with_locality(geoc.geocode(location, exactly_one=False))
                if not result:
                    return {}
                if not result.locality or not result.administrative:
                    # We want the geocoder to give us an canonical name for
                    # this location.  If it hasn't (because the user searched
                    # using a name that doesn't match up to the canonical name,
                    # we use the location to find the canonical name.
                    result = GeocoderController._result_with_locality(geoc.geocode('%f, %f' % (result.latitude, result.longitude), exactly_one=False))
                place, (lat, lng) = result
            except ValueError:
                return {}
        else:
            bbox = asShape(bbox)
            try:
                result = GeocoderController._result_with_locality(geoc.geocode('%f, %f' % (bbox.centroid.y, bbox.centroid.x), exactly_one=False))
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
        geopoint = Point(lng, lat)
        if bbox:
            c.almanacs = self._nearby_almanacs(bbox)
        else:
            c.almanacs = meta.Session.query(Almanac).join(Almanac.pages).distinct().filter(func.st_dwithin(Almanac.location, func.st_transform(func.st_geomfromtext('SRID=%s;POINT(%f %f)' % ('4326', result.longitude, result.latitude)), storage_SRID), 6233)).limit(10).all()
        nearby_kml = render('/almanac/kml.mako')
        return dict(lat=lat, lng=lng, layer=nearby_kml,
                    geojson=simplejson.dumps(geopoint.__geo_interface__),
                    authoritative_name=authoritative_name,
                    name_based=name_based,
                    almanac=almanac)

    def _nearby_almanacs(self, bounds):

        return meta.Session.query(Almanac).join(Almanac.pages).distinct().filter(func.st_intersects(Almanac.location, func.st_transform('SRID=%s;%s' % ('4326', b2a_hex(bounds.to_wkb())), storage_SRID))).limit(10).all()

    @staticmethod
    def _result_with_locality(gen):
        first = None
        for x in gen:
            if not first:
                first = x
            if x and x.locality and x.administrative:
                return x
        return first
