from rest_framework import status
from rest_framework.exceptions import APIException


class TrackingException(Exception):
    pass


class StateMachineChangeNotAllowed(APIException, TrackingException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "StateMachineChangeNotAllowed"
    default_detail = "State change violates the rules"
