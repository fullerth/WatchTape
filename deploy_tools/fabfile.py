from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/fullerth/WatchTape.git'
env.user = 'ubuntu'
env.key_filename = 'mrthrill-superlists.pem'
env.host = 'fiveseconds.tv'

def server():
    """This pushes to the EC2 instance defined below"""
    #EC2 instance IP
    env.host_string = 'watchtape-staging.mcfuller.com'
    # the user on the system
    env.user = 'mrthrill'

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    #_create_directory_structure_if_necessary(site_folder)
    _get_latest_source(site_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def enable():
    env.cwd = '~/sites/{0}'.format(env.host)
    #nginx configuration and enable of site
    run('sed "s/SITENAME/{0}/g" deploy_tools/nginx.template.conf | \
        sudo tee /etc/nginx/sites-available/{0}'.format(env.host))
    #use f tag in case the link already exists
    run('sudo ln -sf ../sites-available/{0} \
        /etc/nginx/sites-enabled/{0}'.format(env.host))

    #upstart configuration for nginx
    run('sed "s/SITENAME/{0}/g" deploy_tools/gunicorn-upstart.template.conf | \
        sudo tee /etc/init/gunicorn-{0}.conf'.format(env.host))

def reload():
    #reload nginx
    run('sudo service nginx reload')
    run('sudo start gunicorn-{0}'.format(env.host))


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(site_folder):
    if exists(site_folder + '/.git'):
        run('cd %s && git fetch' % (site_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, site_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (site_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/WatchTape/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/WatchTape/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
        run('%s/bin/pip install -r %s/../deploy_tools/requirements.txt' % (
            virtualenv_folder, source_folder)
        )

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,)
    )

def _update_database(source_folder):
#     run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
#         source_folder,)
#     )
    run('cd %s && ../virtualenv/bin/python3 manage.py syncdb --noinput' % (
        source_folder,)
    )