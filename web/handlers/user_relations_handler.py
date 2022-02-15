from datetime import datetime


from models import UserRelations, session_scope


def create_friendship(first_user_id: str, second_user_id: str) -> bool:
    """
    Creates a friendship relation between two provided users
    :param first_user_id:
    :param second_user_id:
    :return:
    """
    try:
        friendship = UserRelations(
            first_user_id=first_user_id,
            second_user_id=second_user_id,
            relation_type="FRIENDS",
            created_at=datetime.datetime.utcnow(),
        )
        with session_scope() as _session:
            _session.add(friendship)
            return True
    except Exception as e:
        print(f"One of the users do not exist: {str(e)}")
        return False
