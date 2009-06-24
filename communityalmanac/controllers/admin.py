import logging

from communityalmanac.lib.base import BaseController, render
from communityalmanac import model
from communityalmanac import forms
from communityalmanac.model import meta
from formalchemy.ext.pylons.admin import FormAlchemyAdminController
from repoze.what.predicates import has_permission
from repoze.what.plugins.pylonshq import ControllerProtector

log = logging.getLogger(__name__)

class AdminController(BaseController):
    model = model
    forms = forms
    def Session(self):
        return meta.Session

AdminController = FormAlchemyAdminController(AdminController)
AdminController = ControllerProtector(has_permission('manage'))(AdminController)


from formalchemy.fields import FieldRenderer
from formalchemy.forms import FieldSet
from formalchemy import helpers as h
from shapely import wkb
from shapely.geometry.geo import asShape
import simplejson

class GeoRenderer(FieldRenderer):
    def render(self, **kwargs):
        shape = self.field.model_value
        geo_interface = shape.__geo_interface__
        json = simplejson.dumps(geo_interface)
        return h.text_field(self.name, value=json)

    def _deserialize(self, data):
        json = data
        shape = simplejson.loads(json)
        location = wkb.loads(asShape(shape).to_wkb())
        # uncommenting this causes a transform error
        #location.srid = 4326
        return location


from sqlalchemy import types as sqltypes

FieldSet.default_renderers[model.sqlgeotypes.POINT] = GeoRenderer
FieldSet.default_renderers[sqltypes.NullType] = GeoRenderer
