from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    #avatar = serializers.SerializerMethodField('get_avatar')
    year_display = serializers.Field('get_year_display')
    chapter_id = serializers.Field('chapter_id')
    position = serializers.Field('position.title')
    api_url = serializers.SerializerMethodField('get_api_url')
    get_full_name = serializers.Field('get_full_name')
    is_chapter_admin = serializers.Field('is_chapter_admin')
    profile_image_url = serializers.Field('profile_image_url')
    profile_image_lg_url = serializers.Field('profile_image_lg_url')

    class Meta:
        model = User
        fields = [
            'url',
            'api_url',
            'id',
            'first_name',
            'last_name',
            'get_full_name',
            'profile_image_url',
            'profile_image_lg_url',
            'status',
            'position',
            'is_chapter_admin',
            'email',
            'phone',
            'year',
            'year_display',
            'major',
            'hometown',
            'highschool_gpa',
            'gpa',
            'chapter_id',
            #'fraternity',
            #'university',
            #'groups',
        ]

    def get_api_url(self, obj):
        if obj:
            return "#/users/%s" % obj.id
        else:
            return "#/users/"


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
