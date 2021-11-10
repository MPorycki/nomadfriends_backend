from models import Places, session_scope


def create_place(place_data: dict):
    place = Places(id=place_data["id"], name=place_data["name"],
                   lat=place_data["lat"], lng=place_data["lng"])
    with session_scope() as _session:
        _session.add(place)


def get_place(place_id: str) -> Places:
    with session_scope() as _session:
        return _session.query(Places).filter(Places.id == place_id).first()
