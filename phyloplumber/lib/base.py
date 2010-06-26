"""The base Controller API

Provides the BaseController class for subclassing.
"""
import os

from pylons import config
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from phyloplumber.model.meta import Session

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()


_INTERNAL_DIR = os.path.abspath(os.path.expandvars(os.path.expanduser(config.get('top_internal_dir', '~/internals_phyloplumber'))))
_EXTERNAL_DIR = os.path.abspath(os.path.expandvars(os.path.expanduser(config.get('top_external_dir', '~/phyloplumber'))))


_MISSING_SETTING_MSG = 'A %(setting)s setting is required in the initialization file used to start the server'

def verify_dir(dir):
    if os.path.exists(dir):
        if os.path.isdir(dir):
            return True
        raise OSError("File %(f)s exists, so a directory cannot be created at that location" % {f : dir})
    os.makedirs(dir)

def get_top_internal_dir():
    '''Returns the absolute path to the top directory for "internal" storage.
    
    Raises OSError if the directory does not exist and cannot be created.
    '''
    if not _INTERNAL_DIR:
        raise OSError(_MISSING_SETTING_MSG % {'setting' : 'top_internal_dir'})
    verify_dir(_INTERNAL_DIR)
    return _INTERNAL_DIR

def get_top_external_dir():
    '''Returns the absolute path to the top directory for "external" storage.
    
    Raises OSError if the directory does not exist and cannot be created.
    '''
    if not _EXTERNAL_DIR:
        raise OSError(_MISSING_SETTING_MSG % {'setting' : 'top_external_dir'})
    verify_dir(_EXTERNAL_DIR)
    return _EXTERNAL_DIR
    
