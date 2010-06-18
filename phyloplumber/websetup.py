"""Setup the phyloplumber application"""
import logging

import pylons.test

from phyloplumber.config.environment import load_environment
from phyloplumber.model.meta import Session, get_metadata

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup phyloplumber here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    
    # Create the tables if they don't already exist
    get_metadata().create_all(bind=Session.bind)
