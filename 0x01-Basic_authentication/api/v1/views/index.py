#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    Returns the status of the API.

    Returns:
        str: A JSON response containing the status.

    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    Returns the statistics of the API.

    Returns:
        str: A JSON response containing the statistics.

    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """
    Raises an unauthorized (401) error.

    Raises:
        HTTPException: The unauthorized (401) error.

    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """
    Raises a forbidden (403) error.

    Raises:
        HTTPException: The forbidden (403) error.

    """
    abort(403)
