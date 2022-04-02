import datetime, uuid

from models import Invitations, session_scope


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
