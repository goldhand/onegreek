from rest_framework import serializers

from .models import Chapter


class ChapterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Chapter
        fields = ['awards', 'cost', 'description', 'philanthropy', 'potential_new_members', 'status', 'title']
