from rest_framework import serializers

from .models import Chapter


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    awards = serializers.WritableField(source='awards')
    description = serializers.WritableField(source='description')
    philanthropy = serializers.WritableField(source='philanthropy')
    potential_new_members = serializers.WritableField(source='potential_new_members')

    class Meta:
        model = Chapter
        fields = ['url', 'awards', 'cost', 'description', 'philanthropy', 'potential_new_members', 'status', 'title']
