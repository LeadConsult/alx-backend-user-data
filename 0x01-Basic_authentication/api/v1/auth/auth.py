#!/usr/bin/env python3
""" 
"""

from tabnanny import check
from flask import request
from typing import TypeVar, List
User = TypeVar('User')


class Auth:
    """Handles authentication and authorization."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that are excluded from authentication.

        Returns:
            bool: True if authentication is required, False if the path is excluded.

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
        Retrieves the authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The authorization header value.

        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user.

        Args:
            request: The Flask request object.

        Returns:
            User: The current user.

        """
        return None
