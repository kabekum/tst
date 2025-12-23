# backend/core/permissions.py
from rest_framework import permissions

class IsFirmAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsAttorneyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        return request.user and request.user.is_authenticated and request.user.role in ['senior_lawyer','junior_lawyer','admin']
