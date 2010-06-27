# The projects controller provides an interface for version-controlled projects
#   stored on the fs as subdirectories of 
#   ${top_internal_dir}/projects where top_internal_dir is a variable in the
#   .ini file used to launch the server.
#
# The structure of these directories is assumed to be:
#   name.txt -- plain text file with the user-assigned name of the project
#   index.xml
#
# The name of each project sub-directories is simply a unique number assigned
#   internally by phyloplumber
#
#
import logging, os, sys
import phyloplumber.lib.helpers as h

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from phyloplumber.lib.base import BaseController, render
log = logging.getLogger(__name__)
from phyloplumber.lib.base import get_internal_dir, get_external_dir

def get_project_subdir_names():
    e = get_internal_dir('projects')
    log.debug("Checking %s for subdirectories\n" % e)
    sub = os.listdir(e)
    proj_sub = []
    for i in sub:
        project_dir = os.path.join(e, i)
        if os.path.isdir(project_dir):
            proj_sub.append(i)
    return proj_sub

class ProjectsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')

    def index(self, format='html'):
        """GET /projects: All items in the collection"""
        e = get_internal_dir('projects')
        log.debug("Checking %s for subdirectories\n" % e)
        sub = get_project_subdir_names()
        c.subdirs = []
        for i in sub:
            project_dir = os.path.join(e,i)
            try:
                name_file = os.path.join(project_dir, 'name.txt')
                project_name = open(name_file, 'rU').readlines().strip()
            except:
                project_name = "Corrupted Project"
            entry_tuple = (project_name, h.url(controller='projects', action='show', id=i))
            c.subdirs.append(entry_tuple)
        return render('/projects.html')

    def create(self):
        """POST /projects: Create a new item"""
        # Figure out what the next number to use for the subdirectory -- not guaranteed to be unique across instances, so this is not too crucial
        dir_list = get_project_subdir_names()
        next_ind = 0
        for d in dir_list:
            try:
                i = int(d)
                if i >= next_ind:
                    next_ind = 1 + i
            except:
                pass
        


    def new(self, format='html'):
        """GET /projects/new: Form to create a new item"""
        return render('/new_project.html')

    def update(self, id):
        """PUT /projects/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('project', id=ID),
        #           method='put')
        # url('project', id=ID)

    def delete(self, id):
        """DELETE /projects/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('project', id=ID),
        #           method='delete')
        # url('project', id=ID)
        return u'blah'

    def show(self, id, format='html'):
        """GET /projects/id: Show a specific item"""
        # url('project', id=ID)
        return u'blah'

    def edit(self, id, format='html'):
        """GET /projects/id/edit: Form to edit an existing item"""
        # url('edit_project', id=ID)
