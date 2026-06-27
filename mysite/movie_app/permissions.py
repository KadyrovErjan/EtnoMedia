from rest_framework import permissions

class CheckSubscription(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.access_type == 'free':
            return True
        if request.user.subscription_status == 'VIP':
            return True
        return False


class CheckUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user