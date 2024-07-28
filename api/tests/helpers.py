import random
import string


class User:
    rio_key = None
    api_key = None
    active_url = None
    verified = False
    groups = list()
    success = False

    def __init__(self, in_user_dict=None):
        # If user details are not specified, randomize user
        if in_user_dict is None:
            in_user_dict = dict()
        length = random.randint(3, 20)
        self.username = in_user_dict['Username'] if ('Username' in in_user_dict.keys()) else ''.join(
            random.choices(string.ascii_letters, k=length))
        self.email = in_user_dict['Email'] if ('Email' in in_user_dict.keys()) else ''.join(
            random.choices(string.ascii_letters, k=length)) + "@email.com"
        self.password = in_user_dict['Password'] if ('Password' in in_user_dict.keys()) else ''.join(
            random.choices(string.ascii_letters + string.digits + string.punctuation, k=20))

    # def register(self):
    #     # Post new user
    #     json = {'Username': self.username, 'Email': self.email, 'Password': self.password}
    #     response = requests.post("http://127.0.0.1:5000/register/", json=json)
    #     self.success = (response.status_code == 200)
    #
    #     # Get user info from db
    #     query = 'SELECT * FROM rio_user WHERE username = %s'
    #     params = (self.username,)
    #     result = db.query(query, params)
    #
    #     self.pk = result[0]['id']
    #     self.username = result[0]['username']
    #     self.email = result[0]['email']
    #     self.rk = result[0]['rio_key']
    #     self.url = result[0]['active_url']
    #     self.password = None  # Zero password, even for testing
    #     self.verified = False
    #
    # def verify_user(self):
    #     response = requests.post(f"http://127.0.0.1:5000/verify_email/{self.url}")
    #     # Confirm user is verified
    #     query = 'SELECT * FROM rio_user WHERE username = %s'
    #     params = (self.username,)
    #     result = db.query(query, params)
    #     self.verified = (result[0]['verified'] == True)
    #
    #     self.refresh()
    #
    #     return (response.status_code == 200)
    #
    # def add_to_group(self, group_name):
    #     json = {'username': self.username, 'group_name': group_name, 'ADMIN_KEY': os.getenv('ADMIN_KEY')}
    #     response = requests.post(f"http://127.0.0.1:5000/user_group/add_user", json=json)
    #     success = (response.status_code == 200)
    #
    #     if not success:
    #         return success
    #
    #     self.groups.append('group_name'.lower())
    #     return success
    #
    # def register_api_key(self):
    #     json = {'Username': self.username}
    #     response = requests.post(f"http://127.0.0.1:5000/api_key/register/", json=json)
    #     success = (response.status_code == 200)
    #
    #     if not success:
    #         return success
    #     # Confirm user is verified
    #     query = ('SELECT * '
    #              'FROM api_key '
    #              'JOIN rio_user ON api_key.id = rio_user.api_key_id '
    #              'WHERE rio_user.username = %s ')
    #     params = (self.username,)
    #     result = db.query(query, params)
    #     self.ak = result[0]['api_key']
    #     return success
    #
    # def refresh(self):
    #     query = ('SELECT * FROM rio_user \n'
    #              'WHERE username = %s')
    #     params = (self.username,)
    #     result = db.query(query, params)
    #
    #     self.username = result[0]['username']
    #     self.email = result[0]['email']
    #     self.pk = result[0]['id']
    #     self.url = result[0]['active_url']
    #     self.verified = result[0]['verified']
    #     self.rk = result[0]['rio_key']
    #
    #     query = ('SELECT * FROM rio_user \n'
    #              'JOIN api_key ON api_key.id = rio_user.api_key_id \n'
    #              'WHERE username = %s')
    #     params = (self.username,)
    #     result = db.query(query, params)
    #
    #     if len(result) > 0:
    #         self.ak = result[0]['api_key']
    #     else:
    #         self.ak = None
    #
    #     # User groups
    #     self.groups.clear()
    #     query = ('SELECT * '
    #              'FROM rio_user '
    #              'JOIN user_group_user ON rio_user.id = user_group_user.user_id \n'
    #              'JOIN user_group ON user_group_user.user_group_id = user_group.id \n'
    #              'WHERE rio_user.username = %s ')
    #     params = (self.username,)
    #     result = db.query(query, params)
    #     for result_row in result:
    #         self.groups.append(result_row['name'])
    #
    # def to_dict(self):
    #     return {
    #         'RioUser PK': self.pk,
    #         'Username': self.username,
    #         'Email': self.email,
    #         'RioKey': self.rk,
    #         'APIKey': self.ak,
    #         'URL': self.url,
    #         'Verified': self.verified,
    #         'Groups': self.groups
    #     }