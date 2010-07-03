"""The base Controller API

Provides the BaseController class for subclassing.
"""
import os, logging
log = logging.getLogger(__name__)

from pylons import config
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from phyloplumber.model.meta import Session

class PhlyoplumberError(Exception):
    pass

class InvalidProjectIDError(Exception):
    def __init__(self, project_id):
        self.project_id = project_id
    def __str__(self):
        d = {'i' : self.project_id}
        return '"%(i)s" is not a valid project id' % d
    
class ConfigFileError(PhlyoplumberError):
    def __init__(self, setting_name, msg=''):
        self.setting_name = setting_name
        if msg:
            self.msg = msg
        else:
            self.msg = 'Invalid setting (sorry for the vague, explanation of the error -- alert the authors of phyloplumber that it is issuing an unhelpful message)'
    def __str__(self):
        return 'ConfigFileError: ' + self.message()
    def message(self):
        return 'Error in the "%(setting)s" setting of your configuration file: %(msg)s' % {'setting' : self.setting_name, 'msg' : self.msg}

class CorruptedProjectError(PhlyoplumberError):
    def __init__(self, project_id, msg):
        self.project_id = project_id
        self.msg = msg
    def __str__(self):
        d = {'i' : self.project_id , 'm' : self.msg }
        return 'The project with id="%(i)s" has been corrupted:  %(m)s' % d
    


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

class ServiceController(BaseController):
    pass

def get_boolean_config_var(name):
    '''Checks for 'name' in the config file. Returns True, False, or None'''
    v = config.get(name)
    if v is None:
        return v
    vupper = v.upper()
    if vupper in ['1', 'YES', 'Y', 'T', 'TRUE']:
        return True
    if vupper in ['0', 'NO',  'N', 'F', 'FALSE']:
        return False
    raise ConfigFileError(name, 'Should be "TRUE" or "FALSE", but found "%(v)s"' % {'v' : v})
    
_MISSING_SETTING_MSG = 'A %(setting)s setting is required in the initialization file used to start the server'

def verify_dir(dir):
    if os.path.exists(dir):
        if os.path.isdir(dir):
            return True
        raise OSError("File %(f)s exists, so a directory cannot be created at that location" % {f : dir})
    log.debug("Creating directory " + dir)
    os.makedirs(dir)

def get_top_internal_dir():
    '''Returns the absolute path to the top directory for "internal" storage.
    
    Raises ConfigFileError if the directory does not exist and cannot be created.
    '''
    raw = config.get('top_internal_dir')
    if raw is None:
        log.debug('top_internal_dir not in config')
        log.debug('config = '+ str(config))
        raw = '~/internals_phyloplumber'
    _INTERNAL_DIR = os.path.abspath(os.path.expandvars(os.path.expanduser(raw)))
    if not _INTERNAL_DIR:
        raise ConfigFileError('top_internal_dir', _MISSING_SETTING_MSG % {'setting' : 'top_internal_dir'})
    try:
        verify_dir(_INTERNAL_DIR)
    except OSError, x:
        raise ConfigFileError('top_internal_dir', str(x))        
    return _INTERNAL_DIR

def get_internal_dir(sub):
    parent = get_top_internal_dir()
    full = os.path.join(parent, sub)
    verify_dir(full)
    return full

def get_top_external_dir():
    '''Returns the absolute path to the top directory for "external" storage.
    
    Raises OSError if the directory does not exist and cannot be created.
    '''
    raw = config.get('top_external_dir')
    if raw is None:
        log.debug('top_external_dir not in config')
        log.debug('config = '+ str(config))
        raw = '~/phyloplumber'
    _EXTERNAL_DIR = os.path.abspath(os.path.expandvars(os.path.expanduser(raw)))
    if not _EXTERNAL_DIR:
        raise ConfigFileError('top_external_dir', _MISSING_SETTING_MSG % {'setting' : 'top_external_dir'})
    try:
        verify_dir(_EXTERNAL_DIR)
    except OSError, x:
        raise ConfigFileError('top_external_dir', str(x))        
    return _EXTERNAL_DIR

def get_external_dir(sub):
    parent = get_top_external_dir()
    full = os.path.join(parent, sub)
    verify_dir(full)
    return full

    
def serves_projects():
    '''Returns True if serves_projects configuration setting has a value that evaluates 
    to true.
    '''
    return get_boolean_config_var('serves_projects') is not False

def is_debug_mode():
    '''Returns True if debug configuration setting has a value that evaluates 
    to true.
    '''
    return config.get('debug', False)
