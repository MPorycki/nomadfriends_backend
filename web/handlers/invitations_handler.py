import datetime, uuid

from models import Invitations, session_scope
from web.handlers.user_relations_handler import create_friendship


def create_invitation(inviter_id: str):
    """
    Creates a new invitation generated by the user with inviter_id. Return an Invite object as dict.
    """
    invitation = Invitations(
        id=uuid.uuid4(),
        created_by=inviter_id,
        created_at=datetime.datetime.utcnow(),
        expires_at=(datetime.datetime.utcnow() + datetime.timedelta(days=7)),
    )

    with session_scope() as _session:
        _session.add(invitation)
        return {
            "id": invitation.id,
            "expires_at": str(invitation.expires_at).split(".")[0],
        }


def accept_invitation(invitation_id: str, invitee_id: str) -> dict:
    """
    Creating a user relation between provided users and deleting the invitation afterwards.
    """
    with session_scope() as _session:
        inv = (
            _session.query(Invitations).filter(Invitations.id == invitation_id).first()
        )
        if not inv:
            return {"result": False, "reason": "Invitation could not be found."}
        if is_expired(inv.id, inv.expires_at):
            return {"result": False, "reason": "Invitation had expired."}
        if create_friendship(inv.created_by, invitee_id):
            delete_invitation(inv.id)
            return {"result": True, "reason": "Friendship created succesfully."}
        else:
            return {
                "result": False,
                "reason": "One of the users do not exist or the friendship already exists.",
            }


def delete_invitation(invitation_id: str):
    """
    Remove an invitation with a provided invitation_id
    """
    try:
        with session_scope() as _session:
            _session.query(Invitations).filter(
                Invitations.id == invitation_id
            ).fideleterst()
    except Exception as e:
        pass


def is_expired(invitation_id: str, expires_at: datetime.datetime):
    """
    Checks if a given invitation is already expired and if yes, deletes it.
    """
    if datetime.datetime.utcnow() > expires_at:
        delete_invitation(invitation_id)
        return True
    else:
        return False
