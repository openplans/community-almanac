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
from webhelpers.paginate import Page as PaginationPage
import simplejson

log = logging.getLogger(__name__)

class HomesweethomeController(BaseController):

    def home(self):
        page_idx = request.GET.get('page', 1)
        try:
            page_idx = int(page_idx)
        except ValueError:
            page_idx = 1
        almanac_query = meta.Session.query(Almanac).order_by(Almanac.modified.desc())
        c.pages = Page.latest()
        c.is_homepage = True
        c.pagination = PaginationPage(almanac_query, page=page_idx, items_per_page=10)
        cur_page = c.pagination.page
        next_page = c.pagination.next_page
        prev_page = c.pagination.previous_page
        per_page = c.pagination.items_per_page
        if next_page:
            start = ((next_page-1) * per_page) + 1
            end = start + per_page - 1
            end = min(end, c.pagination.item_count)
            c.next_page_text = '%d - %d' % (start, end)
            c.next_page_url = '%s?page=%s' % (request.path_url, next_page)
        if prev_page:
            start = (prev_page-1) * per_page
            end = (start + per_page - 1) + 1
            start = max(start, 1)
            c.prev_page_text = '%d - %d' % (start, end)
            c.prev_page_url = '%s?page=%s' % (request.path_url, prev_page)
        c.showing_start = ((cur_page-1) * per_page) + 1
        c.showing_end = cur_page * per_page
        c.showing_end = min(c.showing_end, c.pagination.item_count)
        c.almanacs = c.pagination.items
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
