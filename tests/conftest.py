import pytest
from generator import generate_user
from methods.order_methods import OrderMethods
from methods.user_methods import UserMethods

@pytest.fixture
def generate_user_data():
    user_data = generate_user()
    yield user_data
    response = UserMethods.login_user(
        email=user_data['email'],
        password=user_data['password']
    )
    if response.status_code == 200:
        access_token = response.json().get("accessToken")
        UserMethods.delete_user(access_token)

@pytest.fixture
def existent_ingredients():
    response = OrderMethods.get_ingredients()
    ingredients = response.json()["data"]
    buns = [element["_id"] for element in ingredients if element["type"] == "bun"]
    sauces = [element["_id"] for element in ingredients if element["type"] == "sauce"]
    mains = [element["_id"] for element in ingredients if element["type"] == "main"]
    bun = buns[0]
    sauce = sauces[0]
    main = mains[0]
    return {"bun":bun, "sauce": sauce, "main": main}