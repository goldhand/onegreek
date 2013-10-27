from django.contrib.auth.models import Group

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [
            'url', 'first_name', 'last_name', 'phone',
            'year', 'major', 'hometown', 'chapter',
            'highschool_gpa', 'gpa'
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_set = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail')

    class Meta:
        model = Group
        fields = [
            'url', 'name', 'user_set'
        ]
