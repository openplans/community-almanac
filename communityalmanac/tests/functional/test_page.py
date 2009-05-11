from communityalmanac.tests import *
from communityalmanac.model import Almanac
from communityalmanac.model import meta

class TestPageController(TestController):

    def create_almanac(self, name, slug):
        a = Almanac(name, slug)
        meta.Session.save(a)
        meta.Session.commit()
        return a

    def test_create(self):
        almanac = self.create_almanac(u'my almanac for page', 'a4p')
        response = self.app.get(url('page_create', almanac=almanac), status=200)
