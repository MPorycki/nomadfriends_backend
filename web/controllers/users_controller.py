import connexion  # TODO import more specific objects from the lib (less code)
from flask import make_response

from web.handlers.users_handler import (
    create_user,
    edit_user_data,
    login,
    get_all_users,
)


def sign_up() -> set:  # noqa: E501
    """
    Add a new user account
    """
    if connexion.request.is_json:
        response = create_user(user_data=connexion.request.get_json())
        print(response)
    if not response["user"]:
        return response, 401
    resp = make_authentication_response(
        response["user"], response["sessionId"], response["user"]["id"]
    )
    return resp


def handle_login():
    if connexion.request.is_json:
        body = connexion.request.get_json()
        response = login(body["email"], body["password"])
    if not response["user_id"]:
        return response, 401
    resp = make_authentication_response(
        response["user"], response["sessionId"], response["user_id"]
    )
    return resp


def make_authentication_response(body, session_id, user_id):
    resp = make_response(body)
    resp.set_cookie("sessionId", str(session_id), httponly=True)
    resp.set_cookie("userId", str(user_id), httponly=True)
    resp.status_code = 200
    return resp


def handle_get_user():
    pass


def handle_update_user():
    if connexion.request.is_json:
        response = edit_user_data(connexion.request.get_json())
    if not response:
        return "Not all required data was provided.", 400
    return response, 201


def handle_get_all_users():
    response = get_all_users()
    return response, 201


def handle_main():
    return "Hello, world!", 200
