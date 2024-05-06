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

from rest_framework import viewsets
from .models import User, Group
from django.contrib.auth.models import Permission
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer
from .permissions import IsAuthenticatedAndSelfOrIsStaff
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from gdmty_django_users.decorators import recaptcha_verify


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'username']

    def get_serializer_class(self):
        # TODO: poner condicionales para que solo se pueda editar el usuario logueado o si es staff pueda editar a todos
        if self.request.user.is_authenticated:
            return UserSerializer
        else:
            return Response('Unauthorized', status=401)

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        elif self.request.user.is_authenticated:
            return User.objects.filter(username=self.request.user.username)
        else:
            return Response('Unauthorized', status=401)

    @recaptcha_verify('verify')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @recaptcha_verify('verify')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @recaptcha_verify('verify')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    permission_classes = [IsAuthenticatedAndSelfOrIsStaff]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']


class GroupViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        # TODO: poner condicionales para que solo se pueda editar el usuario logueado o si es staff pueda editar a todos
        if self.request.user.is_authenticated:
            return GroupSerializer
        else:
            return Response('Unauthorized', status=401)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Group.objects.all()
        elif self.request.user.is_authenticated:
            return self.request.user.groups.all()
        else:
            return Response('Unauthorized', status=401)

    @recaptcha_verify('verify')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @recaptcha_verify('verify')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    permission_classes = [IsAuthenticatedAndSelfOrIsStaff]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']


class PermissionViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        # TODO: poner condicionales para que solo se pueda editar el usuario logueado o si es staff pueda editar a todos
        if self.request.user.is_authenticated:
            return PermissionSerializer
        else:
            return Response('Unauthorized', status=401)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Permission.objects.all()
        elif self.request.user.is_authenticated:
            return self.request.user.user_permissions.all()
        else:
            return Response('Unauthorized', status=401)

    @recaptcha_verify('verify')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @recaptcha_verify('verify')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    permission_classes = [IsAuthenticatedAndSelfOrIsStaff]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']

