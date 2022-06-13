from http import HTTPStatus

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from service.db import db_session
from service.errors import AppError
from service.views.abilities import ability_view
from service.views.roles import role_view
from service.views.users import user_view


def handle_http_exceptions(error: HTTPException):
    return {'message': error.description}, error.code


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.status


def handle_validation_error(error: ValidationError):
    return error.json(), HTTPStatus.BAD_REQUEST


def shutdown_session(exception=None):
    db_session.remove()


def create_app():
    app = Flask(__name__)

    app.register_blueprint(user_view, url_prefix='/api/v1/users')
    app.register_blueprint(role_view, url_prefix='/api/v1/roles')
    app.register_blueprint(ability_view, url_prefix='/api/v1/abilities')

    app.register_error_handler(HTTPException, handle_http_exceptions)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    app.teardown_appcontext(shutdown_session)

    return app
