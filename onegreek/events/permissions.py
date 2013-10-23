from rest_framework import permissions


class IsOwnerOrViewer(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            if request.user.chapter == obj.get_chapter or request.user.chapter in obj.viewers.all():
                return True

        # Write permissions are only allowed to the owner of the snippet
        if obj.owner == request.user:
            return True