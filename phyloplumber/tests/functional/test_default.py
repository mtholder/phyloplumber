from phyloplumber.tests import *

class TestDefaultController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='default', action='index'))
        # Test response...
