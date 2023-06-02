#!/usr/bin/env python3
"""
SessionDBAuth module for the API
"""
from datetime import datetime, timedelta

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for managing session-based authentication
    with database support.
    """

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session for the given user ID and saves
        it to the database.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID, or None if user_id
            is invalid.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with the given session ID
        from the database.

        Args:
            session_id: The session ID.

        Returns:
            str: The user ID associated with the session ID,
            or None if session_id is invalid
                or the session has expired.
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None
        if self.session_duration <= 0:
            return user_session[0].user_id
        created_at = user_session[0].created_at
        if (created_at + timedelta(seconds=self.session_duration)) \
            < datetime.utcnow():
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys the current session by removing
        it from the database.

        Args:
            request: The request object.

        Returns:
            bool: True if the session was successfully
            destroyed, False otherwise.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_session = UserSession.search({'session_id': session_cookie})
        if len(user_session) == 0:
            return False
        del self.user_id_by_session_id[session_cookie]
        user_session[0].remove()
        return True
