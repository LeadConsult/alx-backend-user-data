#!/usr/bin/env python3
"""
End-to-end integration test
"""
import requests


BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """
    Registers a user with the provided email and password.
    Makes a POST request to the /users endpoint with the user data.
    Asserts that the response status code is 201 (Created).
    """
    response = requests.post(
        f'{BASE_URL}/users',
        json={'email': email, 'password': password})
    assert response.status_code == 201


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with the provided email and password.
    Makes a POST request to the /sessions endpoint with the login data.
    Asserts that the response status code is 401 (Unauthorized).
    """
    response = requests.post(
        f'{BASE_URL}/sessions',
        json={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in a user with the provided email and password.
    Makes a POST request to the /sessions endpoint with the login data.
    Asserts that the response status code is 200 (OK).
    Asserts that the response data contains a 'session_id' field.
    Returns the session ID.
    """
    response = requests.post(
        f'{BASE_URL}/sessions',
        json={'email': email, 'password': password})
    assert response.status_code == 200
    data = response.json()
    assert 'session_id' in data
    return data['session_id']


def profile_unlogged() -> None:
    """
    Retrieves the profile of an unlogged user.
    Makes a GET request to the /profile endpoint.
    Asserts that the response status code is 403 (Forbidden).
    """
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Retrieves the profile of a logged-in user.
    Makes a GET request to the /profile endpoint with the session ID
    in the cookie.
    Asserts that the response status code is 200 (OK).
    Asserts that the response data contains an 'email' field.
    """
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.get(f'{BASE_URL}/profile', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'email' in data


def log_out(session_id: str) -> None:
    """
    Logs out a user with the provided session ID.
    Makes a DELETE request to the /sessions endpoint with the session ID
    in the cookie.
    Asserts that the response status code is 204 (No Content).
    """
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.delete(
        f'{BASE_URL}/sessions', headers=headers)
    assert response.status_code == 204


def reset_password_token(email: str) -> str:
    """
    Requests a reset password token for the user with the provided email.
    Makes a POST request to the /reset_password endpoint with the email data.
    Asserts that the response status code is 200 (OK).
    Asserts that the response data contains an 'email' field
    and a 'reset_token' field.
    Returns the reset token.
    """
    response = requests.post(
        f'{BASE_URL}/reset_password', data={'email': email})
    assert response.status_code == 200
    data = response.json()
    assert 'email' in data and 'reset_token' in data
    return data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the password for the user with the provided email
    using the reset token.
    Makes a PUT request to the /reset_password endpoint with
    the email, reset token, and new password data.
    Asserts that the response status code is 200 (OK).
    Asserts that the response data contains an 'email' field
    and a 'message' field with the value 'Password updated'.
    """
    response = requests.put(
        f'{BASE_URL}/reset_password',
        data={'email': email,
              'reset_token': reset_token,
              'new_password': new_password})
    assert response.status_code == 200
    data = response.json()
    assert 'email' in data and 'message' in data and\
        data['message'] == 'Password updated'


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
