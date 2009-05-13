from communityalmanac.tests import *

class TestGeocoderController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='geocoder', action='index'))
        # Test response...
