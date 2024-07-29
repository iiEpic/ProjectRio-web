import os
import re
import secrets
import string
import subprocess
import sys


def create_django_superuser():
    print('Running Django Create Super User...')
    subprocess.run(['venv/bin/python', 'manage.py', 'createsuperuser', '--username', 'admin', '--email', 'admin@admin.com', '--noinput'])
    with open('.env', 'r') as f:
        password = f.read()
    password = re.search('DJANGO_SUPERUSER_PASSWORD=(.*)$', password).group(1)
    print(f'Created super user:\nUsername: admin\nPassword: {password}\n--------------------')


def create_hidden_env():
    if not os.path.exists('.env'):
        print('Creating .env file...')
        with open('.env', 'w+') as f:
            password = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(8))
            f.write(f'DJANGO_SUPERUSER_PASSWORD={password}')
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = password
    else:
        # Check if we have superuser password in there
        with open('.env', 'r') as f:
            data = f.read()
            if not re.search('DJANGO_SUPERUSER_PASSWORD', data):
                password = ''.join(
                    secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(8))
                f.write(f'DJANGO_SUPERUSER_PASSWORD={password}')
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = re.search('DJANGO_SUPERUSER_PASSWORD=(.*)$', data).group(1)


def create_rio_user():
    print('Creating admin Rio user...')
    subprocess.run(['venv/bin/python', 'manage.py', 'create_test_admin_user'])


def create_virtual_env():
    if not os.path.exists('venv'):
        # Creating venv
        print('Creating virtual environment...')
        subprocess.run([sys.executable, '-m', 'venv', 'venv/'])


def django_migrations():
    print('Running Django Migrations...')
    subprocess.run(['venv/bin/python', 'manage.py', 'makemigrations'])
    subprocess.run(['venv/bin/python', 'manage.py', 'migrate'])


def install_pip_packages():
    print('Installing pip packages to virtual environment...')
    subprocess.run(['venv/bin/python', '-m', 'pip', 'install', '-r', 'requirements.txt'])


def start_webserver():
    print('Starting webserver...')
    subprocess.run(['venv/bin/python', 'manage.py', 'runserver'])


def main():
    # Create a virtual env
    create_virtual_env()

    # Install the pip packages in our venv
    install_pip_packages()

    # Create .env file for admin password
    create_hidden_env()

    # Make Django migrations
    django_migrations()

    # Create superuser
    create_django_superuser()

    # Create RioUser
    create_rio_user()

    # Start webserver
    start_webserver()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--purge':
            print('Removing database...')
            os.remove('db.sqlite3')
    main()
