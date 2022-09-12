from rest_framework import permissions


class TimeLogChangePermission(permissions.BasePermission):
    message = "Logs can be deleted or modified only by creator"

    def has_object_permission(self, request, view, obj):
        return request.user.employee == obj.employee


class TimeLogAddPermission(permissions.BasePermission):
    message = "User can add logs only to tasks assigned to his team"

    def has_object_permission(self, request, view, obj):
        return obj.team_assigned_to == request.user.employee.team
