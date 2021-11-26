import connexion  # TODO import more specific objects from the lib (less code)
from flask import make_response

from settings import DOMAIN
from web.handlers.users_handler import (
    create_user,
    edit_user_data,
    login,
    get_user,
    get_all_users,
    get_user_profile,
    logout,
)
from web.util import is_authorized


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
    if not response["user"]:
        return response, 401
    resp = make_authentication_response(
        response["user"], response["sessionId"], response["user"]["id"]
    )
    return resp


def make_authentication_response(body, session_id, user_id):
    resp = make_response(body)
    resp.headers.add("Access-Control-Allow-Credentials", "true")
    resp.headers.add("Access-Control-Expose-Headers", "Set-Cookie")
    resp.headers.add("Access-Control-Allow-Headers", "Set-Cookie")
    resp.set_cookie(
        key="sessionId",
        value=str(session_id),
        domain=DOMAIN,
        httponly=True,
        samesite=None,
    )
    resp.set_cookie(
        key="userId",
        value=str(user_id),
        domain=DOMAIN,
        httponly=True,
        samesite=None,
    )
    resp.status_code = 200
    return resp


@is_authorized
def handle_session_check():
    response = get_user(connexion.request.cookies["userId"])
    return response, 200


@is_authorized
def handle_get_user():
    response = get_user_profile(connexion.request.cookies["userId"])
    return response, 200


@is_authorized
def handle_update_user():
    if connexion.request.is_json:
        response = edit_user_data(connexion.request.get_json())
    if not response:
        return "Not all required data was provided.", 400
    return response, 200


def handle_get_all_users():
    response = get_all_users()
    return response, 200


@is_authorized
def handle_logout():
    body = logout(
        connexion.request.cookies["sessionId"],
        connexion.request.cookies["userId"],
    )
    resp = make_response(body)
    resp.headers.add("Access-Control-Allow-Credentials", "true")
    resp.headers.add("Access-Control-Expose-Headers", "Set-Cookie")
    resp.headers.add("Access-Control-Allow-Headers", "Set-Cookie")
    resp.set_cookie(
        key="sessionId",
        value="",
        domain=DOMAIN,
        httponly=True,
        samesite=None,
        expires=1,
    )
    resp.set_cookie(
        key="userId",
        value="",
        domain=DOMAIN,
        httponly=True,
        samesite=None,
        expires=1,
    )
    resp.status_code = 200
    return resp


def handle_main():
    return "Hello, world!", 200
