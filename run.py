import os

import connexion

from web import encoder


def create_app():
    abs_file_path = os.path.abspath(os.path.dirname(__file__))
    openapi_path = abs_file_path
    app = connexion.FlaskApp(
        __name__, specification_dir=openapi_path, options={"swagger_ui": True, "serve_spec": True}
    )
    app.add_api("swagger.yml", strict_validation=True)
    flask_app = app.app
    flask_app.json_encoder = encoder.JSONEncoder

    return flask_app
