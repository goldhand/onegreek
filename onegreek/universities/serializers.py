from rest_framework import serializers

from .models import University


class UniversitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = University
        fields = [
            'url', 'title', 'slug',
        ]
