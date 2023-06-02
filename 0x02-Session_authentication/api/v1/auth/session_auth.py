#!/usr/bin/env python3
"""
SessionAuth module for the API
"""
from uuid import uuid4

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class for managing session-based authentication.
    """

    user_id_by_session_id = {}  
    # Dictionary to store user IDs by session IDs

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session for the given user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID, or None if user_id is invalid.
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())  
        
        # Generate a unique session ID
        self.user_id_by_session_id[session_id] = user_id  
        
        # Store the user ID by session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID, or None
            if session_id is invalid.
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current authenticated user based on the session.

        Args:
            request: The request object.

        Returns:
            User: The current authenticated user, or None if not authenticated.
        """
        session_cookie = self.session_cookie(request)  
        
        # Get the session cookie from the request
        user_id = self.user_id_for_session_id(session_cookie)  
        
        # Retrieve the user ID based on the session cookie
        return User.get(user_id)  
        # Retrieve the User instance based on the user ID


    def destroy_session(self, request=None):
        """
        Destroys the current session.

        Args:
            request: The request object.

        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)  
        # Get the session cookie from the request
        if not session_cookie:
            return False
        user_id = self.user_id_for_session_id(session_cookie)  
        # Retrieve the user ID based on the session cookie
        if not user_id:
            return False
        del self.user_id_by_session_id[session_cookie]  
        # Remove the session from the user_id_by_session_id dictionary
        return True
