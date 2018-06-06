from rest_framework.exceptions import APIException


class BadRequestError(APIException):
    status_code = 400
