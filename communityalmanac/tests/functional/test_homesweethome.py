from communityalmanac.tests import *

class TestHomesweethomeController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='homesweethome', action='index'))
        # Test response...
