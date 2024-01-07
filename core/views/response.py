from flask import Response
import json


class BaseResponse(Response):
    """
    Base response class
    """

    def __init__(self, response=None, **kwargs):
        super().__init__(response, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key, value)


class APIDataResponse(BaseResponse):
    """
    API response class
    """

    def __init__(self, data, status_code=200, **kwargs):
        response_payload = {
            "data": data,
            "status_code": status_code,
        }

        super().__init__(
            json.dumps(response_payload),
            status=status_code,
            mimetype="application/json",
            **kwargs
        )


class APIListResponse(BaseResponse):
    """
    API list response class
    """

    def __init__(self, data, count, status_code=200, **kwargs):
        response_payload = {
            "data": data,
            "count": count,
            "status_code": status_code,
        }

        super().__init__(
            json.dumps(response_payload),
            status=status_code,
            mimetype="application/json",
            **kwargs
        )


class APIMessageResponse(BaseResponse):
    """
    API message response class
    """

    def __init__(self, message, description=None, status_code=200, **kwargs):
        response_payload = {
            "message": message,
            "description": description,
            "status_code": status_code,
        }

        super().__init__(
            json.dumps(response_payload),
            status=status_code,
            mimetype="application/json",
            **kwargs
        )


class APIErrorResponse(BaseResponse):
    """
    API error response class
    """

    def __init__(self, error, error_type, description=None, status_code=500, **kwargs):
        response_payload = {
            "error": error,
            "error_type": error_type,
            "description": description,
            "status_code": status_code,
        }

        super().__init__(
            json.dumps(response_payload),
            status=status_code,
            mimetype="application/json",
            **kwargs
        )
