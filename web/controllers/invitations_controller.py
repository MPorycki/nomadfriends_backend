from connexion import request

from web.handlers.invitations_handler import create_invitation
from web.util import is_authorized


@is_authorized
def create_new_invite():
    response = create_invitation(request.cookies["userId"])
    return response, 200
