# Custom error classes
class ValidationError(Exception):
    def __init__(self, error_message, description=None):
        self.error_message = error_message
        self.description = description


class InternalServerError(Exception):
    def __init__(self, error_message, description=None):
        self.error_message = error_message
        self.description = description


class NotFoundError(Exception):
    def __init__(self, error_message, description=None):
        self.error_message = error_message
        self.description = description


class InvalidCredentialsError(Exception):
    def __init__(self, error_message, description=None):
        self.error_message = error_message
        self.description = description


class InvalidUsageError(Exception):
    def __init__(self, error_message, description=None):
        self.error_message = error_message
        self.description = description
