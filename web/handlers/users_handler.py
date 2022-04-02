import datetime
import uuid

from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError

from models import Sessions, Users, session_scope
from web.handlers.trips_handler import get_user_trips


def create_user(user_data: dict) -> dict:
    """
    Registers the user by creating an account record in the database
    :param user_data: Data use to create the user
    :return: Payload with data regarding the result of the sign-up process
    """
    if not user_data["email"] or not user_data["password"]:
        return {"user": None, "reason": "Email or password was not provided"}
    _user_id = uuid.uuid4()
    user = Users(
        id=_user_id,
        email=user_data["email"],
        hashed_password=sha256_crypt.hash(user_data["password"]),
        created_at=datetime.datetime.utcnow(),
    )
    # TODO The user should not be created until the entire response is ready
    # Therefore, creating user, getting its data and creating the session should be
    # in 1 transaction
    try:
        with session_scope() as _session:
            _session.add(user)
    except IntegrityError:
        return {"user": None, "reason": "Email is already taken."}
    return {
        "user": get_user(_user_id),
        "sessionId": create_session_for_user(_user_id),
    }


def login(email: str, raw_password: str) -> dict:
    """
    Logs in the user based on the username and password they provide
    :param email: email of the user
    :param raw_password:direct password inputted by the user into the form
    :return: Session_id and the corresponding account_id or (None, None) if failed
    """
    with session_scope() as session:
        user_id, hashed_password = (
            session.query(Users.id, Users.hashed_password)
            .filter(Users.email == email)
            .first()
        )
    if not user_id:
        return {"user": None, "sessionId": None}
    if sha256_crypt.verify(raw_password, hashed_password):
        return {
            "user": get_user(user_id),
            "sessionId": create_session_for_user(user_id),
        }
    else:
        return {"user": None, "sessionId": None}


def create_session_for_user(_user_id: str):
    """
    Creates session for the given user
    :param _user_id:
    :return: newly created session_id
    """
    _session_id = uuid.uuid4()
    new_session = Sessions(
        user_id=_user_id,
        session_id=_session_id,
        created_at=datetime.datetime.now(),
    )
    with session_scope() as _session:
        _session.add(new_session)
    return _session_id


def logout(_session_id: str, _user_id: str):
    with session_scope() as _session:
        _session.query(Sessions).filter(
            Sessions.session_id == _session_id, Sessions.user_id == _user_id
        ).delete()
    return "User logged out."


def get_user(_user_id: str) -> dict:
    """
    Returns user data as defined in OpenAPI schema.

    :param _user_id = id of the user the data should be returned for.
    :return: Dict with user data according ot the OpenAPI schema
    """
    user = {}
    with session_scope() as session:
        user_profile = session.query(Users).filter(Users.id == _user_id).first()
        user["profile"] = user_profile.as_dict()
        user["id"] = user_profile.id
        user["trips"] = get_user_trips(user["id"])
    return user


def get_user_profile(_user_id: str) -> dict:
    """
    Returns user profile only, as defined in OpenAPI schema
    :param _user_id: Id of the user profile to be returned
    :return:
    """
    with session_scope() as _session:
        user = _session.query(Users).filter(Users.id == _user_id).first()
        if user:
            result = user.as_dict()
            result["userId"] = result.pop("id")  # According to OpenAPI schema
            return result
        else:
            return {}


def get_all_users() -> list:
    """
    Returns the list of all users.
    :return: List with all the users according to the OpenAPI schema
    """
    response = []
    with session_scope() as session:
        users = [user.as_dict() for user in session.query(Users).all()]
        for user in users:
            response.append(
                {
                    "id": user["id"],
                    "profile": user,
                    "trips": get_user_trips(user["id"]),
                }
            )
    return response


def edit_user_data(data: dict) -> dict:
    """
    Updates user object based on provided data
    :param data: Data for all user fields
    :return: Updated user object
    """
    with session_scope() as _session:
        user = _session.query(Users).filter(Users.id == data["userId"]).first()
        try:
            user.email = data["email"]
            user.first_name = data["firstName"]
            user.last_name = data["lastName"]
            user.display_name = data["displayName"]
            user.avatar = data["avatar"]
            user.phone = data["phone"]
            user.date_of_birth = data["dateOfBirth"]
            user.languages = data["languages"]
        except KeyError:
            return None
        response = user.as_dict()
    return response


def session_is_valid(_session_id, _user_id):
    with session_scope() as _session:
        session = (
            _session.query(Sessions)
            .filter(
                Sessions.session_id == _session_id,
                Sessions.user_id == _user_id,
            )
            .first()
        )
        if not session:
            return False
        return True
