from connexion import request

from web.handlers.trips_handler import (
    create_trip,
    get_user_trips,
    delete_user_trips,
)
from web.util import is_authorized


@is_authorized
def handle_get_user_trips():
    response = get_user_trips(request.cookies["userId"])
    return response, 200


@is_authorized
def handle_create_trip():
    if not request.is_json:
        return "No request body", 400
    response = []
    delete_user_trips(
        request.cookies["userId"]
    )  # Quick fix for now, so that FE does not duplicate trips
    for trip in request.get_json():
        response.append(create_trip(trip_data=trip, _user_id=request.cookies["userId"]))
    if not response:
        return "Something went wrong during trip creation", 400
    return response, 200
