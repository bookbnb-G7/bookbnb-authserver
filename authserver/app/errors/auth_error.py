class AuthException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class MissingTokenError(AuthException):
    def __init__(self):
        message = "missing token"
        super().__init__(status_code=400, detail=message)


class RevokedIdTokenError(AuthException):
    def __init__(self):
        message = "token has been revoked"
        super().__init__(status_code=401, detail=message)


class ExpiredIdTokenError(AuthException):
    def __init__(self):
        message = "token has expired"
        super().__init__(status_code=401, detail=message)


class InvalidIdTokenError(AuthException):
    def __init__(self):
        message = "invalid token"
        super().__init__(status_code=401, detail=message)


class RevokedApiKeyError(AuthException):
    def __init__(self):
        message = "revoked API key"
        super().__init__(status_code=401, detail=message)
