from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # TODO verify that user  works or needs user owner_id
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner_id == request.user
