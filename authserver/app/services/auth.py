import os

import app.config as config
from app.errors.auth_error import (ExpiredIdTokenError, InvalidIdTokenError,
                                   MissingTokenError, RevokedApiKeyError,
                                   RevokedIdTokenError)
from firebase_admin import auth


class AuthService:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.firebase_app = config.firebase_authenticate()

    @staticmethod
    def verify_access_token(token):
        if token is None:
            raise MissingTokenError()

        try:
            user_data = auth.verify_id_token(token)
        except auth.RevokedIdTokenError as e:
            raise RevokedIdTokenError() from e
        except auth.ExpiredIdTokenError as e:
            raise ExpiredIdTokenError() from e
        except auth.InvalidIdTokenError as e:
            raise InvalidIdTokenError() from e
        except ValueError as e:
            raise InvalidIdTokenError() from e
        return user_data

    @staticmethod
    def create_user(email, password):
        auth.create_user(email=email, password=password)

    def verify_api_key(self, api_key):
        if api_key == self.api_key:
            return

        raise RevokedApiKeyError()


class AuthServiceFake:
    def __init__(self):
        self.user_data = {
            "email": "lebronjames@gmail.com",
            "uid": "E90qRcXZLbP6QdzcrJrn0fmz5Um1",
        }

        self.expiredToken = False
        self.revokedToken = False
        self.invalidToken = False

        self.api_key = os.environ.get("API_KEY")

    def verify_access_token(self, token):
        if token is None:
            raise MissingTokenError()
        if self.revokedToken:
            raise RevokedIdTokenError()
        if self.expiredToken:
            raise ExpiredIdTokenError()
        if self.invalidToken:
            raise InvalidIdTokenError()
        return self.user_data

    def set_expired_token(self):
        self.expiredToken = True
        self.revokedToken = False
        self.invalidToken = False

    def set_revoked_token(self):
        self.revokedToken = True
        self.expiredToken = False
        self.invalidToken = False

    def set_invalid_token(self):
        self.invalidToken = True
        self.expiredToken = False
        self.revokedToken = False

    def set_valid_token(self):
        self.invalidToken = False
        self.expiredToken = False
        self.revokedToken = False

    def set_user_data(self, data):
        self.user_data = data

    def verify_api_key(self, api_key):
        if api_key == self.api_key:
            return

        raise RevokedApiKeyError()


auth_service = None
if os.environ.get("ENVIRONMENT") == "production":
    auth_service = AuthService()
else:
    auth_service = AuthServiceFake()
