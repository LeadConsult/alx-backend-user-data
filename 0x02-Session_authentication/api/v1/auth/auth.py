#!/usr/bin/env python3
"""
Auth module for API
"""
import re
from os import getenv
from typing import List, TypeVar

from flask import request


class Auth:
    """
    Authentication class for handling user authentication.
    """

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
            path (str): The path to check.
            exclude_paths (List[str]): List of paths to exclude from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or exclude_paths is None or exclude_paths == []:
            return True
        
        # Add trailing slash to the path if it doesn't have one
        path = path + '/' if path[-1] != '/' else path
        
        # Iterate over the exclude paths and check if the current path matches any of them
        for exclude_path in exclude_paths:
            # Convert the exclude path to a regular expression pattern
            exclude_path = exclude_path.replace('/', '\\/').replace('*', '.*')
            regex = re.compile(exclude_path)
            
            # Check if the current path matches the exclude path pattern
            if regex.search(path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.

        Args:
            request: The request object.

        Returns:
            str: The value of the Authorization header, or None if not found.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current authenticated user.

        Args:
            request: The request object.

        Returns:
            TypeVar('User'): The current authenticated user, or None if not authenticated.
        """
        return None

    def session_cookie(self, request=None):
        """
        Get the session cookie value from the request.

        Args:
            request: The request object.

        Returns:
            The value of the session cookie, or None if not found.
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
