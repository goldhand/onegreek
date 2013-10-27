from rest_framework import serializers

from .models import Chapter


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    awards = serializers.WritableField(source='awards')
    description = serializers.WritableField(source='description')
    philanthropy = serializers.WritableField(source='philanthropy')
    potential_new_members = serializers.WritableField(source='potential_new_members')

    class Meta:
        model = Chapter
        fields = ['url', 'title', 'awards', 'cost', 'description', 'gpa', 'philanthropy', 'potential_new_members', 'status', 'group']
