import os
import re
import secrets
import string
import subprocess
import sys


class Startup:
    def __init__(self):
        if not os.path.exists('venv'):
            # Creating venv
            print('Creating virtual environment...')
            subprocess.run([sys.executable, '-m', 'venv', 'venv/'])

        if os.path.exists(os.path.join(os.getcwd(), 'venv', 'Scripts')):
            # Using the /venv/Scripts/ environment
            self.python_venv = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')
        else:
            # Using the /venv/bin/ environment
            self.python_venv = os.path.join(os.getcwd(), 'venv', 'bin', 'python')

        print('Installing pip packages to virtual environment...')
        subprocess.run([self.python_venv, '-m', 'pip', 'install', '-r', 'requirements.txt'])

        self.create_hidden_env()

        print('Running Django Migrations...')
        subprocess.run([self.python_venv, 'manage.py', 'makemigrations'])
        subprocess.run([self.python_venv, 'manage.py', 'migrate'])

        print('Running Django Create Super User...')
        subprocess.run(
            [self.python_venv, 'manage.py', 'createsuperuser', '--username', 'admin', '--email', 'admin@admin.com',
             '--noinput'])
        with open('.env', 'r') as f:
            password = f.read()
        password = re.search('DJANGO_SUPERUSER_PASSWORD=(.*)$', password).group(1)
        print(f'Created super user:\nUsername: admin\nPassword: {password}\n--------------------')

        print('Creating admin Rio user...')
        subprocess.run([self.python_venv, 'manage.py', 'create_test_admin_user'])

        print('Populating database with default data...')
        subprocess.run([self.python_venv, 'manage.py', 'db_setup'])

        print('Starting webserver...')
        subprocess.run([self.python_venv, 'manage.py', 'runserver'])

    def create_hidden_env(self):
        if not os.path.exists('.env'):
            print('Creating .env file...')
            with open('.env', 'w+') as f:
                password = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(8))
                f.write(f'\nDJANGO_SUPERUSER_PASSWORD={password}\n')
            os.environ['DJANGO_SUPERUSER_PASSWORD'] = password
        else:
            # Check if we have superuser password in there
            with open('.env', 'r') as f:
                data = f.read()

            if not re.search('DJANGO_SUPERUSER_PASSWORD', data):
                password = ''.join(
                    secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(8))
                with open('.env', 'a+') as f:
                    f.write(f'\nDJANGO_SUPERUSER_PASSWORD={password}\n')
            else:
                password = re.search('DJANGO_SUPERUSER_PASSWORD=(.*)$', data).group(1)
            os.environ['DJANGO_SUPERUSER_PASSWORD'] = password


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--purge':
            print('Removing database...')
            os.remove('db.sqlite3')

    Startup()
