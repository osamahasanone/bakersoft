from rest_framework import status
from rest_framework.exceptions import APIException


class TrackingException(Exception):
    pass


class LogActionNotAllowed(APIException, TrackingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "LogActionNotAllowed"
    default_detail = "User can't modify or delete other users logs"


class TaskIsAssignedToAnotherTeam(APIException, TrackingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "TaskIsAssignedToAnotherTeam"
    default_detail = (
        "User can't add logs to a task that is assigned to another team"  # Noqa
    )
