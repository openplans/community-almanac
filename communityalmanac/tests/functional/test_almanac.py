from communityalmanac.tests import *

class TestAlmanacController(TestController):

    def test_home(self):
        response = self.app.get(url('home'), status=200)

    def test_create(self):
        response = self.app.get(url('almanac_create'), status=200)
        create_form = response.forms[0]
        create_form.set('name', u'my almanac')
        response = create_form.submit()
        self.assertEqual(302, response.status_int)
        response = response.follow(status=200)
