from rest_framework import permissions
from library.models import User

class IsLibrarian(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == User.LIBRARIAN:
            return True
        return False
