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
import logging, os, sys, uuid
import phyloplumber.lib.helpers as h
import formencode
from formencode import htmlfill

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from phyloplumber.model import meta, PhyloplumberProject

from phyloplumber.lib.index_nexml import new_index

from phyloplumber.lib.base import BaseController, render, is_debug_mode, CorruptedProjectError, InvalidProjectIDError
log = logging.getLogger(__name__)
from phyloplumber.lib.base import get_internal_dir, get_external_dir, serves_projects
import dendropy


class ProjectWrapper(object):
    def __init__(self, project_id, dir):
        self.dir = dir
        self.project_id = project_id
        self.name = read_name_for_project(dir)
        index_file = os.path.join(self.dir, 'index.xml')
        try:
            inp = open(index_file, 'rU')
        except:
            if os.path.exists(self.dir):
                raise CorruptedProjectError(project_id, 'index file missing')
            raise InvalidProjectIDError(project_id)
        try:
            self.data_set = dendropy.DataSet(stream=inp, schema='nexml')
        except Exception, x:
            raise CorruptedProjectError(project_id, 'Error parsing the index file:\n' + str(x))
    def get_entities(self):
        return []
    entity_list = property(get_entities)
class NewProjectForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.validators.UnicodeString(not_empty=True)

def get_internal_projects_dir():
    return get_internal_dir('projects')

def get_project_subdir_names():
    e = get_internal_projects_dir()
    log.debug("Checking %s for subdirectories\n" % e)
    sub = os.listdir(e)
    proj_sub = []
    for i in sub:
        project_dir = os.path.join(e, i)
        if os.path.isdir(project_dir):
            proj_sub.append(i)
    return proj_sub

def next_project_id():
    dir_list = get_project_subdir_names()
    next_ind = 0
    for d in dir_list:
        try:
            i = int(d)
            if i >= next_ind:
                next_ind = 1 + i
        except:
            pass
    dirname = str(uuid.uuid4())
    return dirname

def get_relative_dir_for_project(project_id):
    return project_id

def read_project(project_id):
    dir_fragment = get_relative_dir_for_project(project_id)
    dir = os.path.join(get_internal_projects_dir(), dir_fragment)
    return ProjectWrapper(project_id=project_id, dir=dir)
    
    
def read_name_for_project(project_dir):
    try:
        name_file = os.path.join(project_dir, 'name.txt')
        return open(name_file, 'rU').read().strip()
    except:
        return "Corrupted Project"

def get_project_summary_tuple(i):
    e = get_internal_dir('projects')
    project_dir = os.path.join(e,i)
    project_name = read_name_for_project(project_dir)
    return (project_name, h.url(controller='projects', action='show', id=i), i)

class ProjectsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')

    def index(self, format='html'):
        """GET /projects: All items in the collection"""
        if not serves_projects():
            response.status = '403 Forbidden (projects not enabled for this phyloplumber instance)'
            return 'Projects not enabled for this phyloplumber instance'
        sub = get_project_subdir_names()
        c.subdirs = [get_project_summary_tuple(i) for i in sub]
        return render('/projects.html')

    def create(self):
        """POST /projects: Create a new item"""
        # Figure out what the next number to use for the subdirectory -- not guaranteed to be unique across instances, so this is not too crucial
        if not serves_projects():
            response.status = '403 Forbidden (projects not enabled for this phyloplumber instance)'
            return 'Projects not enabled for this phyloplumber instance'
        schema = NewProjectForm()
        try:
            c.form_result = schema.to_python(dict(request.params))
        except formencode.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            html = render('/new_project.html')
            return htmlfill.render(
                html,
                defaults=c.form_result,
                errors=c.form_errors
            )
        
        
        dirname = next_project_id()
        full_path_to_dir = get_internal_dir(os.path.join('projects', dirname))
        p_proj = PhyloplumberProject()
        p_proj.id = dirname
        p_proj.parent_dirname = dirname
        try:
            meta.Session.save(p_proj)
        finally:
            meta.Session.commit()
        log.debug('proj_id = %(id)s\nparent_dirname = %(dir)s\n' % {'id' : p_proj.id , 'dir' : dirname})
        
        log.debug('request.params = %(p)s\n' % {'p' : str(request.params)})
        name = request.params.get('name')
             
        description = request.params.get('description')
        full_path_to_index = os.path.join(full_path_to_dir, 'index.xml')
        
        out = open(full_path_to_index, 'w')
        out.write(new_index(name, project_description=description, project_id=p_proj.id))
        out.close()
        out = open(os.path.join(full_path_to_dir, 'name.txt'), 'w')
        out.write(name + '\n')
        out.close()
        
        new_index(name, description)
        fn = request.params.get('file')
        if fn:
            pass
        out_format = request.params.get('format', 'html')
        response.status_int = 201
        if out_format == 'xml':
            c.subdirs = [get_project_summary_tuple(i)]
            return render('/projects.xml')
        u = url(controller="projects", action='show', id=str(p_proj.id))
        redirect(u)


    def new(self, format='html'):
        """GET /projects/new: Form to create a new item"""
        if not serves_projects():
            response.status = '403 Forbidden (projects not enabled for this phyloplumber instance)'
            return 'Projects not enabled for this phyloplumber instance'
        c.debug = is_debug_mode()
        return render('/new_project.html')

    def update(self, id):
        """PUT /projects/id: Update an existing item"""
        if not serves_projects():
            response.status = '403 Forbidden (projects not enabled for this phyloplumber instance)'
            return 'Projects not enabled for this phyloplumber instance'
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('project', id=ID),
        #           method='put')
        # url('project', id=ID)

    def delete(self, id):
        """DELETE /projects/id: Delete an existing item"""
        if not serves_projects():
            response.status = '403 Forbidden (projects not enabled for this phyloplumber instance)'
            return 'Projects not enabled for this phyloplumber instance'
        #  Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('project', id=ID),
        #           method='delete')
        # url('project', id=ID)
        return u'blah delete'

    def show(self, id, format='html'):
        """GET /projects/id: Show a specific item"""
        if not serves_projects():
            response.status = '403 Forbidden (projects not enabled for this phyloplumber instance)'
            return 'Projects not enabled for this phyloplumber instance'
        c.project = read_project(id)
        return render('/show_project.html')

    def edit(self, id, format='html'):
        """GET /projects/id/edit: Form to edit an existing item"""
        if not serves_projects():
            response.status = '403 Forbidden (projects not enabled for this phyloplumber instance)'
            return 'Projects not enabled for this phyloplumber instance'
        # url('edit_project', id=ID)
