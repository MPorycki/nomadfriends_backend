from models import Places, session_scope


def create_or_get_place_if_exists(place_data: dict) -> dict:
    if not place_exists(place_data["id"]):
        create_place(place_data)
    return get_place(place_data["id"])


def create_place(place_data: dict):
    place = Places(
        id=place_data["id"],
        name=place_data["name"],
        lat=place_data["lat"],
        lng=place_data["lng"],
    )
    with session_scope() as _session:
        _session.add(place)


def get_place(place_id: str) -> Places:
    with session_scope() as _session:
        return (
            _session.query(Places)
            .filter(Places.id == place_id)
            .first()
            .as_dict()
        )


def place_exists(place_id: str) -> bool:
    with session_scope() as _session:
        exists_instance = (
            _session.query(Places).filter(Places.id == place_id).exists()
        )
        return _session.query(exists_instance).scalar()
