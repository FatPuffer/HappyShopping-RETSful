from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        :param request:
        :param view:
        :param obj: 数据库模型对象
        :return: True  or  False
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
