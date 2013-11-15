from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    avatar = serializers.SerializerMethodField('get_avatar')
    year_display = serializers.Field('get_year_display')
    get_full_name = serializers.Field('get_full_name')

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'first_name',
            'last_name',
            'get_full_name',
            'avatar',
            'email',
            'phone',
            'year',
            'year_display',
            'major',
            'hometown',
            'highschool_gpa',
            'gpa',
            'chapter',
            'fraternity',
            'university',
            #'groups',
        ]

    def get_avatar(self, obj):
        if obj:
            try:
                avatar = obj.avatar_set.get(primary=True).get_absolute_url()
            except ObjectDoesNotExist:
                avatar = '/static/img/holderjs-40x40.png'
            return avatar
        else:
            return ''


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_set = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = [
            'id', 'url', 'name', 'user_set'
        ]


class GroupUpdateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = [
            'id', 'url', 'name', 'user_set'
        ]

class GroupCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = [
            'id', 'url', 'name'
        ]
