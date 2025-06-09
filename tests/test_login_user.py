import allure
import pytest
from methods.user_methods import UserMethods

class TestLoginUser:
    @allure.title('Авторизация существующего пользователя')
    def test_successful_login(self, generate_user_data):
        UserMethods.create_user(
            email=generate_user_data["email"],
            password=generate_user_data["password"],
            name=generate_user_data["name"]
        )
        with allure.step('Авторизация пользователя по email и паролю'):
            response = UserMethods.login_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"]
            )
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Авторизация с неверными данными')
    @pytest.mark.parametrize("email_sample, password_sample, case", [
        ("wrong_", "", "email"),
        ("", "wrongpassword", "пароль"),
        ("wrong_", "wrongpassword", "email и пароль"),
    ],)
    def test_login_with_wrong_data(self, generate_user_data, email_sample, password_sample, case):
        with allure.step('Регистрация пользователя'):
            UserMethods.create_user(
                email=generate_user_data["email"],
                password=generate_user_data["password"],
                name=generate_user_data["name"]
            )
        test_email = (email_sample + generate_user_data["email"] if email_sample else generate_user_data["email"])
        test_password = (password_sample if password_sample else generate_user_data["password"])
        with allure.step(f"Попытка авторизации, вводя неверный: {case}"):
            response = UserMethods.login_user(email=test_email, password=test_password)
        assert response.status_code == 401
        assert response.json().get("message") == "email or password are incorrect"
