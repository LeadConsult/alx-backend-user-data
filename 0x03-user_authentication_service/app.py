#!/usr/bin/env python3
"""
Basic Flask app
"""
from auth import Auth
from flask import (
    Flask,
    request,
    abort,
    jsonify,
    redirect
)


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    Returns a JSON response with a welcome message.
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    Registers a new user with the provided email and password.
    Returns a JSON response with the email and a success message
    if the user is created successfully.
    Returns a JSON response with an error message if the email
    is already registered.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Logs in a user with the provided email and password.
    Returns a JSON response with the email and a success
    message if the login is successful.
    Returns a 401 Unauthorized error if the login fails.
    Sets a session ID cookie in the response headers.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({'email': f'{email}', 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Logs out the current user.
    Deletes the session ID cookie from the response headers.
    Redirects to the index page after successful logout.
    Returns a 403 Forbidden error if the user is not logged in.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        response = jsonify({'message': 'logout successful'})
        response.delete_cookie('session_id')
        return redirect('/', code=302)
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Retrieves the profile of the current user.
    Returns a JSON response with the user's email if the user is logged in.
    Returns a 403 Forbidden error if the user is not logged in.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Sends a reset password token to the provided email address.
    Returns a JSON response with the email and the reset token if successful.
    Returns a 403 Forbidden error if the email address is invalid.
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Updates the password for the provided email address with the reset token.
    Returns a JSON response with the email and a success message if the
    password is updated successfully.
    Returns a 403 Forbidden error if the email address or reset token is
    invalid.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'Password updated'}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
