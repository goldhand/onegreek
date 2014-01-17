from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import User




class UserSerializer(serializers.HyperlinkedModelSerializer):

    #avatar = serializers.SerializerMethodField('get_avatar')
    year_display = serializers.Field('get_year_display')
    chapter_id = serializers.Field('chapter_id')
    position = serializers.Field('position.title')
    get_full_name = serializers.Field('get_full_name')
    is_chapter_admin = serializers.Field('is_chapter_admin')
    profile_image_url = serializers.Field('profile_image_url')
    profile_image_lg_url = serializers.Field('profile_image_lg_url')
    fb_photos = serializers.Field('fb_photos')
    fb_access_token = serializers.Field('get_fb_access_token')
    fb_extra_data = serializers.Field('get_fb_extra_data')
    ctype_id = serializers.SerializerMethodField('get_content_type_id')
    #text_color_class = serializers.Field('get_status_text_class')
    name = serializers.Field('name')
    api_url = serializers.Field('get_api_url')
    status_display = serializers.Field('get_status_display')

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'api_url',
            'name',
            'ctype_id',
            'first_name',
            'last_name',
            'get_full_name',
            'profile_img_id',
            'profile_img_src',
            'profile_img_pic',
            'profile_img_select',
            'profile_image_url',
            'profile_image_lg_url',
            'fb_photos',
            'fb_access_token',
            'fb_extra_data',
            'status',
            'status_display',
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


    def get_content_type_id(self, obj):
        return ContentType.objects.get_for_model(User).id


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
