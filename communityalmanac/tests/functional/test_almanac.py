from communityalmanac.tests import *

class TestAlmanacController(TestController):

    def test_home(self):
        response = self.app.get(url('home'), status=200)
        # Test response...
