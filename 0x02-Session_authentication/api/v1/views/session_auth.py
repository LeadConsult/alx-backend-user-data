#!/usr/bin/env python3

"""
Session Authentication Views
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    User login endpoint using session authentication.
    """
    # Retrieve user email and password from the request form
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    
    # Check if email is provided
    if not user_email:
        return jsonify(error="email missing"), 400
    
    # Check if password is provided
    if not user_pwd:
        return jsonify(error="password missing"), 400
    
    try:
        # Search for the user with the provided email
        user = User.search({"email": user_email})
    except Exception:
        return jsonify(error="no user found for this email"), 404
    
    if not user:
        return jsonify(error="no user found for this email"), 404
    
    # Iterate over the found users and check if the password is valid
    for u in user:
        if u.is_valid_password(user_pwd):
            user_id = u.id
            from api.v1.app import auth
            # Create a session for the authenticated user
            session_id = auth.create_session(user_id)
            
            # Create a response with the user JSON data
            response = jsonify(u.to_json())
            
            # Set the session ID as a cookie in the response
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            
            return response
        else:
            return jsonify(error="wrong password"), 401
    
    return jsonify(error="no user found for this email"), 404


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    User logout endpoint using session authentication.
    """
    from api.v1.app import auth
    
    # Destroy the session for the current user
    if auth.destroy_session(request):
        return jsonify({}), 200
    
    abort(404)
