import logging

from binascii import a2b_hex, b2a_hex
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from communityalmanac.lib.base import BaseController, render
from communityalmanac.lib import helpers as h
from communityalmanac.model import Almanac
from communityalmanac.model import Page
from communityalmanac.model import meta
from communityalmanac.model.meta import storage_SRID
from pylons.decorators.cache import beaker_cache
from sqlalchemy.orm import eagerload
from sqlalchemy.sql import func
from shapely import wkb
from shapely.geometry.geo import asShape
import simplejson

log = logging.getLogger(__name__)

class HomesweethomeController(BaseController):

    def home(self):
        page_idx = request.GET.get('page', 1)
        try:
            page_idx = int(page_idx)
        except ValueError:
            page_idx = 1
        almanac_query = meta.Session.query(Almanac).join(Almanac.pages).distinct().order_by(Almanac.modified.desc())
        c.count = almanac_query.count()
        h.setup_pagination(almanac_query, page_idx)
        c.almanacs = c.pagination.items
        # Almanacs are slightly smaller on the page, we need to show slightly less so that the almanacs are resting on the shelf.
        c.pages = Page.latest(limit=(max(len(c.almanacs)-2,0)))
        c.is_homepage = True
        return render('/home.mako')

    @beaker_cache(expire=120, query_args=True)
    def almanacs_kml(self):
        json = request.params.get('extent')
        # We need to make sure we only select almanacs with pages here,
        query = meta.Session.query(Almanac).join(Almanac.pages).distinct()
        # ... and eager-load the pages since the ktml template uses them.
        query = query.options(eagerload(Almanac.pages))

        # Tried also with contains_eager, not sure what the difference is
        # but I only get a fraction of the expected almanacs:
        #query = meta.Session.query(Almanac).join(Almanac.pages).distinct()
        #query = query.options(contains_eager(Almanac.pages))

        # Also tried using a single, second query for the pages.
        # ... NOPE, requires sqlalchemy > 0.6.0 which blows up on us,
        # maybe not compatible w/ pylons 0.9.7?
        #query = meta.Session.query(Almanac).join(Almanac.pages).distinct()
        #query = query.options(subqueryload(Almanac.pages))

        # Tried also without the explicit join().distinct(), this gives
        # back all almanac whether they have any pages or not:
        #query = meta.Session.query(Almanac).options(eagerload(Almanac.pages))

        if json is not None:
            shape = simplejson.loads(json)
            # Stupid asShape returns an Adapter instead of a Geometry.  We round
            # trip it through wkb to get the correct type.
            bbox = wkb.loads(asShape(shape).to_wkb())
            query = query.filter(func.st_intersects(Almanac.location, func.st_transform('SRID=%s;%s' % ('4326', b2a_hex(bbox.to_wkb())), storage_SRID)))

        c.almanacs = query.order_by(Almanac.modified.desc()).limit(200).all()
        response.content_type = 'application/vnd.google-earth.kml+xml kml'
        return render('/almanac/kml.mako')

    def almanacs_kml_link(self):
        response.content_type = 'application/vnd.google-earth.kml+xml kml'
        return render('/almanac/kml_link.mako')
