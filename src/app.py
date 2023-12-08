import os

from dotenv import dotenv_values
from flask import Flask

from .auth import jwt
from .config import Config
from .extensions import bcrypt, cors, db, migrate
from .routerefs import register_blueprints


def create_app():
    app = Flask(import_name=__name__, instance_relative_config=True)

    __dotenv_vals = dotenv_values(".flaskenv")

    conf = Config(
        json_path=os.path.join(
            app.instance_path, __dotenv_vals.get("CONFIG_FILENAME")  # type: ignore
        )
    )
    app.config.from_object(obj=conf)

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    cors.init_app(app=app)
    bcrypt.init_app(app=app)
    jwt.init_app(app=app)

    app = register_blueprints(app=app)

    setattr(app.json, "sort_keys", False)
    return app
