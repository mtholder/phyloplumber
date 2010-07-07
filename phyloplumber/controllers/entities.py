import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from phyloplumber.lib.base import BaseController, render

log = logging.getLogger(__name__)

class EntitiesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('entity', 'entities')

    def index(self, project_id, format='html'):
        """GET /entities: All items in the collection"""
        # url('entities')
        return 'TODO project_id = ' + project_id

    def create(self, project_id):
        """POST /entities: Create a new item"""
        # url('entities')
        return 'TODO project_id = ' + project_id

    def new(self, project_id, format='html'):
        """GET /entities/new: Form to create a new item"""
        # url('new_entity')
        return 'TODO project_id = ' + project_id

    def update(self, project_id, id):
        """PUT /entities/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('entity', id=ID),
        #           method='put')
        # url('entity', id=ID)
        return 'TODO project_id = ' + project_id + '\nid = ' + id

    def delete(self, project_id, id):
        """DELETE /entities/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('entity', id=ID),
        #           method='delete')
        # url('entity', id=ID)
        return 'TODO project_id = ' + project_id + '\nid = ' + id

    def show(self, project_id, id, format='html'):
        """GET /entities/id: Show a specific item"""
        # url('entity', id=ID)
        return 'TODO project_id = ' + project_id + '\nid = ' + id

    def edit(self, project_id, id, format='html'):
        """GET /entities/id/edit: Form to edit an existing item"""
        # url('edit_entity', id=ID)
        return 'TODO project_id = ' + project_id, + '\nid = ' + id
