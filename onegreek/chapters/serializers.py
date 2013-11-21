from rest_framework import serializers
from django.core.urlresolvers import reverse_lazy, reverse

from .models import Chapter


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    awards = serializers.WritableField(source='awards')
    description = serializers.WritableField(source='description')
    philanthropy = serializers.WritableField(source='philanthropy')
    potential_new_members = serializers.WritableField(source='potential_new_members')
    university_id = serializers.Field('university_id')
    fraternity_id = serializers.Field('fraternity_id')
    linked_group_id = serializers.Field('linked_group_id')
    linked_rush_group_id = serializers.Field('linked_rush_group_id')
    linked_pending_group_id = serializers.Field('linked_pending_group_id')
    api_url = serializers.SerializerMethodField('get_api_url')
    rush_url = serializers.SerializerMethodField('get_rush_url')
    user_count = serializers.SerializerMethodField('get_user_count')

    class Meta:
        model = Chapter
        fields = [
            'id',
            'url',
            'api_url',
            'rush_url',
            'title',
            'slug',
            'user_count',
            'description',
            'awards',
            'philanthropy',
            'potential_new_members',
            'cost',
            'gpa',
            'status',
            #'fraternity',
            #'university',
            'fraternity_id',
            'fraternity_title',
            'university_id',
            'university_title',
            'groups',
            'linked_group_id',
            'linked_rush_group_id',
            'linked_pending_group_id',
        ]

    def get_api_url(self, obj):
        if obj:
            return "#/chapters/%s" % obj.id
        else:
            return "#/chapters/"

    def get_rush_url(self, obj):
        if obj:
            return reverse('chapters:rush', kwargs={'pk': obj.id})
        else:
            return "/chapters/rush/"

    def get_user_count(self, obj):
        if obj:
            return obj.user_set.count()
        else:
            return 0
