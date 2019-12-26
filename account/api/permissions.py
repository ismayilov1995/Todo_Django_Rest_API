from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    message = "You must be logout saw this page"

    def has_permission(self, request, view):
        return not request.user.is_authenticated

class IsOwner(BasePermission):
    message = "You must be owener delete this todo"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # Istifadeci sadece oz todosunu sile bilsin
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CanAddIfOwner(BasePermission):
    message = "You must be owener for delete or add task to this todo"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # Istifadeci sadece oz todosunu sile bilsin
    def has_object_permission(self, request, view, obj):
        print('hazirki', 'sahib')
        print(request.user, obj.user)
        return obj.user == request.user