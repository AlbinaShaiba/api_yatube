from rest_framework import permissions


class AuthorEditOrReadOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_object_permission(self, request, view, obj):

        if obj.author == request.user:
            return True
        
        return False
    