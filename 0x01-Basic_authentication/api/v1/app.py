#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE") == "auth":
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles the 404 (Not found) error.

    Args:
        error: The error object.

    Returns:
        str: A JSON response with the error message and status code.

    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles the 401 (Unauthorized) error.

    Args:
        error: The error object.

    Returns:
        str: A JSON response with the error message and status code.

    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def unauthorized(error) -> str:
    """
    Handles the 403 (Forbidden) error.

    Args:
        error: The error object.

    Returns:
        str: A JSON response with the error message and status code.

    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    Performs actions before each request.

    """
    authorized_list = ['/api/v1/status/',
                       '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if auth and auth.require_auth(request.path, authorized_list):
        if not auth.authorization_header(request):
            abort(401)
        if not auth.current_user(request):
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
