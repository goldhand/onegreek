from rest_framework import serializers

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

    class Meta:
        model = Chapter
        fields = ['url',
                  'title',
                  'slug',
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
                  'university_id',
                  'groups',
                  'linked_group_id',
                  'linked_rush_group_id',
        ]

