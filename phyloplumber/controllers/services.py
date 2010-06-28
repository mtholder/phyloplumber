import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from phyloplumber.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ServicesController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/services.mako')
        # or, return a string
        return 'Hello World'
