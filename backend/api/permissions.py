from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # TODO verify that user  works or needs user owner_id
        # if request.method == POST:
        #     # do some logic to check if the user is not in any team or the owner of the org
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner_id == request.user
