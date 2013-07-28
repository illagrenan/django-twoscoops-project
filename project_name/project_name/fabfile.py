# -*- encoding: utf-8 -*-

import imp
import sys

from fabric.context_managers import cd
from fabric.operations import prompt, run, local, os
from fabric.state import env


def _remove_dir_char(old_string):
    """
    Remove "/" from given string
    :type old_string: str
    """

    dic_to_replace = {os.sep: '', '/': ''}

    for i, j in dic_to_replace.iteritems():
        old_string = old_string.replace(i, j)

    return old_string


full_path = os.path.realpath(__file__)
current_directory = os.path.dirname(__file__)

# Ex: "example_com"
PROJECT_NAME = os.path.dirname(full_path).split(os.sep)[-1] + '/'


def _get_settings_system_path():
    return PROJECT_NAME + 'settings' + '/'


try:
    fabric_settings = imp.load_source('settings',
                                      os.path.join(current_directory, _get_settings_system_path() + 'fabric.py'))
except IOError, e:
    print e
    print 'Error, cannot import settings'
    sys.exit()



###############
# Settings
###############

# The Elastic IP to your server
env.host_string = fabric_settings.HOST

# your user on that system
env.user = fabric_settings.SSH_USER

# Assumes that your *.pem key is in the same directory as your fabfile.py
env.key_filename = fabric_settings.CERTIFICATE_FILE

env.use_ssh_config = True

###############
# End of Settings
###############

##############################
# Internal functions
##############################

def _touch_wsgi():
    run('touch wsgi.py')


def _update_git():
    run('git reset --hard')
    run('git pull')


def _install_pip_requirements(update_requirements):
    if update_requirements:
        extra_options = ' --upgrade'
    else:
        extra_options = ''

    _virtualenv_run('pip install -r requirements/production.txt' + extra_options)


def _update_database():
    run('python manage.py syncdb --migrate --settings=' + _remove_dir_char(PROJECT_NAME) + '.settings.production')
    # run('python manage.py migrate --settings=' + _remove_dir_char(PROJECT_NAME) + '.settings.production')


def _virtualenv_run(command):
    run('source /opt/Envs/{{ project_name }}/bin/activate' + ' && ' + command)

def _update_django_project(update_requirements):
    """ Updates the remote django project.
    """
    with cd(fabric_settings.ROOT_SERVER_DIR + PROJECT_NAME):
        _update_git()

        _install_pip_requirements(update_requirements)


        run('find . -name \*.pyc -delete')
        with cd(fabric_settings.ROOT_SERVER_DIR + PROJECT_NAME + PROJECT_NAME):
            _update_database()
            run('python manage.py collectstatic --noinput --settings=' + _remove_dir_char(
                PROJECT_NAME) + '.settings.production')
            with cd(fabric_settings.ROOT_SERVER_DIR + PROJECT_NAME + PROJECT_NAME + PROJECT_NAME):
                _touch_wsgi()

##############################
# End of Internal functions
##############################

def deploy():
    """
    Deploy Django Project.
    """
    update_requirements = prompt("Update requirements? ", default='no', validate=r'^(yes|no)$')

    if update_requirements == 'no':
        update_requirements = False
        print ("Requirements will NOT be updated")
    elif update_requirements == 'yes':
        update_requirements = True
        print ("Requirements WILL BE updated")

    _update_django_project(update_requirements)


def commit():
    """
    Add all, comit and push.
    """
    commit_message = prompt("Commit message: ")

    local('git add .')
    local('git commit -m "%s"' % commit_message)
    local('git push')