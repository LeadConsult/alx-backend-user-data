#!/usr/bin/env python3
"""
BasicAuth module for API
"""
from base64 import b64decode
from typing import Tuple, TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    A basic auth class to manage the API authentication using Basic Auth.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts and returns the base64 part of the Authorization header for Basic Auth.

        Args:
            authorization_header (str): The Authorization header value.

        Returns:
            str: The base64 part of the Authorization header, or None if not found.
        """
        if authorization_header is None or type(authorization_header) is not str \
            or authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes and returns the decoded value of a Base64 string.

        Args:
            base64_authorization_header (str): The base64 encoded string.

        Returns:
            str: The decoded value, or None if decoding fails.
        """
        if base64_authorization_header is None or type(base64_authorization_header) is not str:
            return None
        try:
            b64_bytes = b64decode(base64_authorization_header)
            return b64_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts and returns the user credentials from the decoded Base64 string.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.

        Returns:
            Tuple[str, str]: The user credentials as a tuple (username, password),
            or (None, None) if not found.
        """
        if decoded_base64_authorization_header is None or type(decoded_base64_authorization_header) \
            is not str or ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns a User instance based on the provided email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The User instance if a matching user is found, otherwise None.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            match = User.search({'email': user_email})
            if len(match) == 0:
                return None
            user = match[0]
            if user.is_valid_password(user_pwd):
                return user
        except Exception:
            pass
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current authenticated user based on the Basic Auth credentials.

        Args:
            request: The request object.

        Returns:
            TypeVar('User'): The current authenticated user, or None if not authenticated
            or invalid credentials.
        """
        header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_credentials = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_credentials[0], user_credentials[1])
