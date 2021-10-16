import connexion
import six

from web.handlers.users_handler import create_user, login


def sign_up() -> set:  # noqa: E501
    """Add a new user account

    """
    if connexion.request.is_json:
        response = create_user(user_data=connexion.request.get_json())
        print(response)
    if not response["user"]:
        return response, 401
    return response, 201


def handle_login():
    if connexion.request.is_json:
        body = connexion.request.get_json()
        response = login(body["email"], body["password"])
    if not response["user_id"]:
        return response, 401
    return response, 201


def handle_get_user():
    pass


def handle_update_user():
    pass


def handle_get_all_users():
    pass


def handle_main():
    return "Hello, world!", 200
