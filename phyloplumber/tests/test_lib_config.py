"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
import sys
from unittest import TestCase
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import url
from routes.util import URLGenerator
from webtest import TestApp
import pylons.test

from phyloplumber.lib.base import get_top_internal_dir, get_top_external_dir


__all__ = ['environ', 'url', 'TestController']

environ = {}

class TestController(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)
    def test_get_top_internal_dir(self):
        x = get_top_internal_dir()
        sys.stderr.write("get_top_internal_dir=%s\n" % str(x))
        self.assertTrue(bool(get_top_internal_dir()))
    def test_get_top_external_dir(self):
        x = get_top_external_dir()
        sys.stderr.write("get_get_top_external_dir()=%s\n" % str(x))
        self.assertTrue(bool(x))
        

