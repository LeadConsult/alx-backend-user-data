#!/usr/bin/env python3
"""
SessionAuth
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    This class handles session-based authentication.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a new session for the specified user.

        Args:
            user_id: ID of the user

        Returns:
            Session ID (UUID) associated with the user's session
        """
        if not user_id or type(user_id) != str:
            return

        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[user_id] = session_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve the user ID associated with the specified session ID.

        Args:
            session_id: Session ID (UUID)

        Returns:
            User ID associated with the session ID
        """
        if not session_id or type(session_id) != str:
            return

        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user based on the provided request.

        Args:
            request: HTTP request object

        Returns:
            User object representing the current user
        """
        if request:
            session_cookie = self.session_cookie(request)
            if session_cookie:
                user_id = self.user_id_for_session_id(session_cookie)
                return User.get(user_id)
     
    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
