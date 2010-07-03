"""Setup the phyloplumber application"""
import logging
import os
import shutil
from phyloplumber.config.environment import load_environment

import pylons.test
#if not pylons.test.pylonsapp:
#    load_environment(conf.global_conf, conf.local_conf)

from phyloplumber.config.environment import load_environment
from phyloplumber.model.meta import Session, get_metadata

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    
    # Create the tables if they don't already exist
    get_metadata().create_all(bind=Session.bind)

    services_parent = conf.get('phyloplumber_services_parent')
    u = conf.get('symlink_phyloplumber_services')
    use_symlink = u and (u.upper() in ['1', 'T', 'Y', 'TRUE', 'YES'])
    if use_symlink:
        install_cmd = os.symlink
    else:
        install_cmd = shutil.copy2

    if services_parent:
        installed_services_file = os.path.join(services_parent, 'phyloplumber_services', 'installed.txt')
        dest_dir = os.path.join(conf['here'], 'phyloplumber', 'controllers')
        template_dest_dir = os.path.join(conf['here'], 'phyloplumber', 'service_templates')
        if os.path.exists(installed_services_file):
            for line in open(installed_services_file, 'rU'):
                n = line.strip()
                if not n:
                    continue
                py_name = n + '.py'
                src_dir = os.path.join(services_parent, 'phyloplumber_services', n)
                src = os.path.join(src_dir, py_name)
                if os.path.exists(src):
                    dest = os.path.join(dest_dir, py_name)
                    if os.path.exists(dest):
                        log.warn('"%(dest)s" exists, this controller is not being replaced' % {'dest' : dest}) 
                    else:
                        install_cmd(src, dest)
                    templates_dir = os.path.join(src_dir, 'templates')
                    if not os.path.exists(templates_dir):
                        continue
                    for f in os.path.listdir(templates_dir):
                        dest = os.path.join(template_dest_dir, f)
                        if os.path.exists(dest):
                            log.warn('"%(dest)s" exists, this template is not being replaced' % {'dest' : dest}) 
                        else:
                            src = os.path.join(templates_dir, f)
                            install_cmd(src, dest)
                else:
                    log.warn('Installed service %(service)s not found at %(path)s' % {'service' : n, 'path' : src})
                    
        
