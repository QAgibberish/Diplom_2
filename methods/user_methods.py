import requests
from data import Url

class UserMethods:
    @staticmethod
    def create_user(email, password, name):
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return requests.post(Url.USER_CREATE, json=payload)

    @staticmethod
    def login_user(email, password):
        payload = {
            "email": email,
            "password": password
        }
        return requests.post(Url.USER_LOGIN, json=payload)

    @staticmethod
    def delete_user(access_token):
        headers = {
            "Authorization": access_token
        }
        return requests.delete(Url.USER_DELETE, headers=headers)