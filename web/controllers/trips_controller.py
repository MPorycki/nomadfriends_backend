from connexion import request

from web.handlers.trips_handler import create_trip


def handle_get_user_trips():
    pass


def handle_create_trip():
    if not request.is_json:
        return "No request body", 400

    for trip in request.get_json():
        response = create_trip(trip_data=trip, _user_id=request.headers["userId"])
    if not response:
        return "Something went wrong during trip creation", 400
    return response, 200
