from django.contrib.auth.models import Group

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [
            'url',
            'first_name',
            'last_name',
            'email',
            'phone',
            'year',
            'major',
            'hometown',
            'highschool_gpa',
            'gpa',
            'chapter',
            'fraternity',
            'university',
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_set = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail')

    class Meta:
        model = Group
        fields = [
            'url', 'name', 'user_set'
        ]
