from communityalmanac.tests import *

class TestAlmanacController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='almanac', action='index'))
        # Test response...
