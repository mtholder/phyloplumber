import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from phyloplumber.lib.base import BaseController, render

log = logging.getLogger(__name__)
from phyloplumber.lib.base import serves_projects

class DefaultController(BaseController):

    def index(self):
        if serves_projects():
            redirect(url(controller='projects', action='index'))
        else:
            redirect(url(controller='services', action='index'))
