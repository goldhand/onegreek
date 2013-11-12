from rest_framework import serializers

from .models import Chapter


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    awards = serializers.WritableField(source='awards')
    description = serializers.WritableField(source='description')
    philanthropy = serializers.WritableField(source='philanthropy')
    potential_new_members = serializers.WritableField(source='potential_new_members')

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
                  'fraternity',
                  'university',
                  'groups',
                  'linked_group',
        ]

