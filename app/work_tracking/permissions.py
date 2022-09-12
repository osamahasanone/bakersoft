from rest_framework import permissions

from work_tracking.services.team import get_team_leader


class TimeLogChangePermission(permissions.BasePermission):
    message = "Logs can be deleted or modified only by creator"

    def has_object_permission(self, request, view, obj):
        return request.user.employee == obj.employee


class TimeLogAddPermission(permissions.BasePermission):
    message = "User can add logs only to tasks assigned to his team"

    def has_object_permission(self, request, view, obj):
        return not obj.task or obj.task.team_assigned_to == request.user.employee.team


class TaskTransitionPermission(permissions.BasePermission):
    message = "Only team leaders can change task status"

    def has_object_permission(self, request, view, obj):
        return request.user.employee == get_team_leader(obj.team_assigned_to)
