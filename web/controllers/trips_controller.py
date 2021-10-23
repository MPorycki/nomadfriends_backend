from connexion import request
from web.handlers.trips_handler import create_trip


def handle_get_user_trips():
    pass


def handle_create_trip():
    if request.is_json:
        for trip in request.get_json():
            response = create_trip(trip_data=trip, _user_id=request.headers["userId"])
    if not response:
        return "Trips not created", 400
    return "Trips created successfully", 200
