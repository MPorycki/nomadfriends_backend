from datetime import datetime

from sqlalchemy import or_

from models import UserRelations, session_scope, Users
from web.handlers.trips_handler import get_user_trips


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


def get_friends_of_user(user_id: str):
    """
    Provides a list of users, that are friends with the provided users
    :param user_id: Id of the user, whose friends are to be found
    :return:
    """
    response = []
    with session_scope() as session:
        friend_ids_one = session.query(UserRelations.second_user_id).filter(
            UserRelations.first_user_id == user_id
        )
        friend_ids_two = session.query(UserRelations.first_user_id).filter(
            UserRelations.second_user_id == user_id
        )
        user_friends = [
            user.as_dict()
            for user in session.query(Users).filter(
                or_(Users.id.in_(friend_ids_one), Users.id.in_(friend_ids_two))
            )
        ]
        for user in user_friends:
            response.append(
                {
                    "id": user["id"],
                    "profile": user,
                    "trips": get_user_trips(user["id"]),
                }
            )
    return response
