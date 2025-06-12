import allure
from methods.order_methods import OrderMethods
from methods.user_methods import UserMethods


class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией')
    def test_create_order_authorized(self, generate_user_data, existent_ingredients):
        UserMethods.create_user(
            email=generate_user_data["email"],
            password=generate_user_data["password"],
            name=generate_user_data["name"]
        )
        with allure.step('Авторизация пользователя'):
            auth = UserMethods.login_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"]
            )
        access_token = auth.json()['accessToken']
        ingredients = [
            existent_ingredients["bun"],
            existent_ingredients["sauce"],
            existent_ingredients["main"]
        ]
        with allure.step('Создание заказа'):
            response = OrderMethods.create_order(
                ingredients=ingredients,
                token=access_token
            )
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Создание заказа без авторизации')
    def test_create_order_unauthorized(self, existent_ingredients):
        ingredients = [
            existent_ingredients["bun"],
            existent_ingredients["sauce"],
            existent_ingredients["main"]
        ]
        with allure.step('Создание заказа без токена'):
            response = OrderMethods.create_order(
                ingredients=ingredients,
                token=None
            )
            assert response.status_code == 401
            assert "order" not in response.json()

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_empty_burger(self, generate_user_data):
        UserMethods.create_user(
            email=generate_user_data["email"],
            password=generate_user_data["password"],
            name=generate_user_data["name"]
        )
        with allure.step('Авторизация пользователя'):
            auth = UserMethods.login_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"]
            )
        access_token = auth.json()['accessToken']
        with allure.step('Создание заказа без ингредиентов'):
            response = OrderMethods.create_order(
                ingredients=[],
                token=access_token
            )
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_wrong_hash(self, generate_user_data):
        UserMethods.create_user(
            email=generate_user_data["email"],
            password=generate_user_data["password"],
            name=generate_user_data["name"]
        )
        with allure.step('Авторизация пользователя'):
            auth = UserMethods.login_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"]
            )
        access_token = auth.json()['accessToken']
        with allure.step('Создание заказа с несуществующими ингредиентами'):
            response = OrderMethods.create_order(
                ingredients=["invalid_bun", "invalid_sauce", "invalid_main"],
                token=access_token
            )
        assert response.status_code == 500
