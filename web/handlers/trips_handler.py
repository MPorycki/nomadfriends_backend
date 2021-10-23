import uuid

from models import Trips, session_scope
from web.handlers.places_handler import create_place, get_place


def get_user_trips(user_id):
    pass


def create_trip(trip_data: dict, _user_id: str) -> bool:
    """
    Creates a new trip for a given user
    :param trip_data: Trip data according to swagger schema
    :param _user_id: Id of the user for whom the trip should be created
    :return:
    """
    if not get_place(trip_data["place"]["id"]):
        create_place(trip_data["place"])
    trip = Trips(id=uuid.uuid4(), user_id=_user_id, arrival_at=trip_data["arrivalAt"],
                 place_id=trip_data["place"]["id"], departure_at=None)
    with session_scope() as _session:
        _session.add(trip)
    return True
