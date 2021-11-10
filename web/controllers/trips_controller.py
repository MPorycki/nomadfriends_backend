from connexion import request

from web.handlers.trips_handler import create_trip, get_user_trips


def handle_get_user_trips():
    response = get_user_trips(request.cookies["userId"])
    return response, 200


def handle_create_trip():
    if not request.is_json:
        return "No request body", 400
    response = []
    for trip in request.get_json():
        response.append(create_trip(trip_data=trip, _user_id=request.cookies["userId"]))
    if not response:
        return "Something went wrong during trip creation", 400
    return response, 200
