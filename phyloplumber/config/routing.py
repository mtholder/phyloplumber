"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'],
                 explicit=True
                 )
    map.minimization = False
    map.minimize = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.resource('project', 'projects')
    map.connect('/', controller='default', action='index')
    map.connect('/projects', controller='projects', action='index')
    map.connect('/entities/{project_id}', controller='entities', action='index')
    map.connect('/entity/{project_id}', controller='entities', action='index')
    map.connect('/entities/{project_id}/create', controller='entities', action='create', method='PUT')
    map.connect('/entity/{project_id}/create', controller='entities', action='create', method='PUT')
    map.connect('/entities/{project_id}/new', controller='entities', action='new')
    map.connect('/entity/{project_id}/new', controller='entities', action='new')
    map.connect('/entity/{project_id}/update/{id}', controller='entities', action='update', method='PUT')
    map.connect('/entity/{project_id}/delete/{id}', controller='entities', action='delete')
    map.connect('/entity/{project_id}/show/{id}', controller='entities', action='show')
    map.connect('/entity/{project_id}/edit/{id}', controller='entities', action='edit')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    return map

