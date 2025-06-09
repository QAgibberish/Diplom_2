import requests
from data import Url

class OrderMethods:
    @staticmethod
    def create_order(ingredients, token=None):
        headers = {}
        if token: headers["Authorization"] = token
        return requests.post(Url.ORDER_CREATE, json={"ingredients": ingredients}, headers=headers)


    @staticmethod
    def get_ingredients():
        return requests.get(Url.GET_INGREDIENTS)