#!-*- coding: utf-8 -*-
"""
Authentication backend for Django's Administration panel users based on email and password
This packages adds features such as group permissions and reCaptcha enterprise token verification.

This package is published as free software under the terms of the Apache License, Version 2.0. Is developed by
Dirección de Gobierno Digital of the Secretaría de Innovación y Gobierno Abierto of Municipality of Monterrey.

Authors: ['César Benjamín García Martínez <mathereall@gmail.com>', 'Miguel Angel Hernández Cortés
<miguelhdezc12@gmail.com>', 'César Guillermo Vázquez Álvarez <chechar.2001@gmail.com>']
Email: gobiernodigital@monterrey.gob.mx
GitHub: https://github.com/gobiernodigitalmonterrey/gdmty-drf-firebase-auth
Package: gdmty_django_users
PyPi: https://pypi.org/project/gdmty-django-users/
License: Apache 2.0

"""

from django.contrib import admin
from django.contrib.auth.models import Group as GroupDjango
from .models import User, Group
from django.contrib.auth.admin import UserAdmin as UserAdminDjango

admin.site.register(Group)
admin.site.unregister(GroupDjango)


@admin.register(User)
class UserAdmin(UserAdminDjango):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(username=request.user.username)

    def get_object(self, request, obj, from_field=None):
        if request.user.is_superuser:
            return super().get_object(request, obj, from_field)
        else:
            if request.user.username == obj:
                return super().get_object(request, obj, from_field)
            return None

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        else:
            if obj is None:
                return []
            else:
                return ['username', 'email', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined',
                        'last_login', 'is_superuser']

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fields(request, obj)
        else:
            if obj is None:
                return []
            else:
                return ['username', 'password', 'first_name', 'last_name']

