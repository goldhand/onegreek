from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'first_name', 'last_name', 'phone', 'highschool_gpa', 'gpa', 'year', 'major', 'hometown', 'chapter']
