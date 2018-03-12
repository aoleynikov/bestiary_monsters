import requests
import json


class TestUserManager:
    @staticmethod
    def create_and_authorize():
        user = {'email': 'test_user@mail.com', 'password': 'testpass'}
        requests.post('http://auth:5000/register',
                      data=json.dumps(user),
                      headers={'content-type': 'application/json'})

        login_response = requests.post('http://auth:5000/login',
                                       data=json.dumps(user),
                                       headers={'content-type': 'application/json'})
        return json.loads(login_response.text)['token']

    @staticmethod
    def clean_up(token):
        requests.delete('http://auth:5000/',
                        headers={'Authorization': 'Bearer ' + token})
