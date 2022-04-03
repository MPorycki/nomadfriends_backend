from connexion import request

from web.handlers.invitations_handler import accept_invitation, create_invitation
from web.util import is_authorized


@is_authorized
def create_new_invite():
    response = create_invitation(request.cookies["userId"])
    return response, 200


@is_authorized
def handle_accept_invitation(id: str):
    response = accept_invitation(id, request.cookies["userId"])
    if response:
        return "Users are friends", 200
    else:
        return "Friendship not created", 404
