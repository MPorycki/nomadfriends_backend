import uuid

from models import Trips, session_scope
from web.handlers.places_handler import (
    create_or_get_place_if_exists,
    get_place,
)


def get_user_trips(_user_id: str) -> list:
    result = []
    with session_scope() as _session:
        trips = _session.query(Trips).filter(Trips.user_id == _user_id).all()
        for trip in trips:
            to_append = trip.as_dict()
            result.append(to_append)
    for trip in result:
        trip["place"] = get_place(trip["placeId"])
        trip.pop("placeId")
    return result


def create_trip(trip_data: dict, _user_id: str) -> dict:
    """
    Creates a new trip for a given user
    :param trip_data: Trip data according to swagger schema
    :param _user_id: Id of the user for whom the trip should be created
    :return:
    """
    try:
        place = create_or_get_place_if_exists(trip_data["place"])
        trip = Trips(
            id=uuid.uuid4(),
            user_id=_user_id,
            arrival_at=trip_data["arrivalAt"],
            place_id=trip_data["place"]["id"],
            departure_at=None,
        )
        with session_scope() as _session:
            _session.add(trip)
            result = trip.as_dict()
            result.pop("placeId")
            result["place"] = place
            return result
    except KeyError as e:
        print(f"Missing input: {str(e)}")
        return None


def delete_user_trips(_user_id: str):
    with session_scope() as _session:
        _session.query(Trips).filter(Trips.user_id == _user_id).delete()
