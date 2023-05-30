#!/usr/bin/env python3
"""
Auth class
"""

from tabnanny import check
from flask import request
from typing import TypeVar, List
from os import getenv
User = TypeVar('User')


class Auth:
    """
    This class provides authentication functionalities.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the specified path.

        Args:
            path: Requested path
            excluded_paths: List of paths that do not require authentication

        Returns:
            True if authentication is required, False otherwise
        """
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the authorization header from the request.

        Args:
            request: HTTP request object

        Returns:
            Authorization header value
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Retrieve the current user based on the provided request.

        Args:
            request: HTTP request object

        Returns:
            User object representing the current user
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieve the session cookie from the request.

        Args:
            request: HTTP request object

        Returns:
            Value of the session cookie
        """
        if request:
            session_name = getenv("SESSION_NAME")
            return request.cookie.get(session_name, None)
