#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    Database class for managing user data.
    """

    def __init__(self) -> None:
        """
        Initializes the database and creates necessary tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Returns the session object for interacting with the database.
        If the session is not initialized, it creates a new session.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database with the provided email
        and hashed password.
        Returns the created user object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database based on the provided
        keyword arguments.
        Returns the found user object.
        Raises NoResultFound if no user is found.
        Raises InvalidRequestError if the query is invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates the user with the provided user ID using the
        provided keyword arguments.
        Raises a ValueError if any of the provided keyword
        arguments are invalid.
        """
        user: User = self.find_user_by(id=user_id)
        for key in kwargs:
            if hasattr(user, key):
                setattr(user, key, kwargs[key])
            else:
                raise ValueError()
        self._session.commit()
