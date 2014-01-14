from django.contrib.contenttypes.models import ContentType
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
    linked_active_group_id = serializers.Field('linked_active_group_id')
    linked_pending_group_id = serializers.Field('linked_pending_group_id')
    linked_pledge_group_id = serializers.Field('linked_pledge_group_id')
    linked_rush_group_id = serializers.Field('linked_rush_group_id')
    linked_call_group_id = serializers.Field('linked_call_group_id')
    linked_admin_group_id = serializers.Field('linked_admin_group_id')
    rush_url = serializers.SerializerMethodField('get_rush_url')
    rush_form_url = serializers.SerializerMethodField('get_rush_form_url')
    rush_form_id = serializers.SerializerMethodField('get_rush_form_id')
    absolute_url = serializers.Field('get_absolute_url')
    groups = serializers.Field('get_groups')
    user_count = serializers.SerializerMethodField('get_user_count')
    chapter_count = serializers.Field('get_chapter_count')
    chapter_rush_count = serializers.Field('get_chapter_rush_count')
    active_count = serializers.Field('get_active_count')
    pledge_count = serializers.Field('get_pledge_count')
    rush_count = serializers.Field('get_rush_count')
    call_count = serializers.Field('get_call_count')
    ctype_id = serializers.SerializerMethodField('get_content_type_id')
    name = serializers.Field('name')
    api_url = serializers.Field('get_api_url')
    average_gpa = serializers.Field('get_chapter_gpa')

    class Meta:
        model = Chapter
        fields = [
            'id',
            'ctype_id',
            'url',
            'api_url',
            'name',
            'rush_url',
            'rush_form_url',
            'rush_form_id',
            'absolute_url',
            'title',
            'slug',
            'user_count',
            'chapter_count',
            'chapter_rush_count',
            'active_count',
            'pledge_count',
            'rush_count',
            'call_count',
            'description',
            'chapter_website',
            'founding_year',
            'chapter_address',
            'awards',
            'philanthropy',
            'potential_new_members',
            'cost',
            'gpa',
            'average_gpa',
            'status',
            'fraternity_id',
            'fraternity_title',
            'university_id',
            'university_title',
            'groups',
            'linked_group_id',
            'linked_active_group_id',
            'linked_pending_group_id',
            'linked_pledge_group_id',
            'linked_rush_group_id',
            'linked_call_group_id',
            'linked_admin_group_id',
        ]


    def get_rush_url(self, obj):
        if obj:
            return reverse('chapters:rush', kwargs={'pk': obj.id})

    def get_rush_form_url(self, obj):
        if obj:
            rush_form = obj.get_rush_form()
            return reverse('rush-forms:detail', kwargs={'pk': rush_form.id})

    def get_rush_form_id(self, obj):
        if obj:
            rush_form = obj.get_rush_form()
            return rush_form.id

    def get_user_count(self, obj):
        if obj:
            return obj.user_set.count()
        else:
            return 0

    def get_content_type_id(self, obj):
        return ContentType.objects.get_for_model(Chapter).id
