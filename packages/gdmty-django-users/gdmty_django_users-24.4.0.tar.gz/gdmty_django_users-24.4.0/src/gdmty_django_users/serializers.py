from rest_framework import serializers
from .models import User, Group
from django.contrib.auth.models import Permission

#


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'user_permissions', 'safe_delete',
                   'is_active']
        read_only_fields = ['last_login', 'username', 'date_joined', 'email', 'groups']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'first_name', 'last_name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
