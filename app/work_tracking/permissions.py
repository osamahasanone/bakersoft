from rest_framework import permissions

from work_tracking.services.team import get_team_leader


class TaskTransitionPermission(permissions.BasePermission):
    message = "Only team leaders can change task status"

    def has_object_permission(self, request, view, obj):
        return request.user.employee == get_team_leader(obj.team_assigned_to)
