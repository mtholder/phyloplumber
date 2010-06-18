import os
from pylons import config

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
    
