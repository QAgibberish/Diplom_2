import allure
import pytest
from methods.user_methods import UserMethods

class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    def test_successful_creation(self, generate_user_data):
        with allure.step('Создание пользователя'):
            response = UserMethods.create_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"],
                name=generate_user_data["name"]
            )
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_duplicate(self, generate_user_data):
        with allure.step('Создание пользователя'):
            UserMethods.create_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"],
                name=generate_user_data["name"]
            )
        with allure.step('Повторное создание пользователя'):
            response = UserMethods.create_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"],
                name=generate_user_data["name"]
            )
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title('Создание пользователя без обязательного поля')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_creation_missing_required_fields(self, field, generate_user_data):
        email = generate_user_data['email'] if field != 'email' else ""
        password = generate_user_data['password'] if field != 'password' else ""
        name = generate_user_data['name'] if field != 'name' else ""
        with allure.step(f"Попытка создать пользователя без поля: {field}"):
            response = UserMethods.create_user(email=email, password=password, name=name)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"