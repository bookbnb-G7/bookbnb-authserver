class BookbnbException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class EmailAlreadyInUseError(BookbnbException):
    def __init__(self, email):
        message = f"email {email} already in use"
        super().__init__(status_code=200, detail=message)
