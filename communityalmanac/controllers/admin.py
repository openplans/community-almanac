import logging

from communityalmanac.lib.base import BaseController, render
from communityalmanac import model
from communityalmanac import forms
from communityalmanac.model import meta
from formalchemy.ext.pylons.admin import FormAlchemyAdminController

log = logging.getLogger(__name__)

class AdminController(BaseController):
    model = model
    forms = forms
    def Session(self):
        return meta.Session

AdminController = FormAlchemyAdminController(AdminController)
