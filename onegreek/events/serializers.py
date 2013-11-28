from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', blank=True)
    title = serializers.WritableField(source='title', blank=True)
    description = serializers.WritableField(source='description', blank=True)
    chapter = serializers.HyperlinkedRelatedField('get_chapter', view_name='chapter-detail', read_only=True)
    attend_url = serializers.Field('get_attend_url')
    rsvp_url = serializers.Field('get_rsvp_url')
    text_color_class = serializers.Field('get_status_text_class')

    class Meta:
        model = Event
        fields = [
            'id',
            'url',
            'title',
            'slug',
            'status',
            'description',
            'start',
            'end',
            'owner',
            'attend_url',
            'rsvp_url',
            'text_color_class',
            #'enable_comments',
            #'viewers',
            #'attendees',
            #'chapter',
        ]


class EventNestedSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', blank=True)
    title = serializers.WritableField(source='title', blank=True)
    description = serializers.WritableField(source='description', blank=True)
    chapter = serializers.HyperlinkedRelatedField('get_chapter', view_name='chapter-detail', read_only=True)
    attend_url = serializers.Field('get_attend_url')
    rsvp_url = serializers.Field('get_rsvp_url')
    text_color_class = serializers.Field('get_status_text_class')
    get_attendees = UserSerializer(many=True)
    get_rsvps = UserSerializer(many=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'url',
            'title',
            'slug',
            'status',
            'description',
            'start',
            'end',
            'owner',
            'attend_url',
            'rsvp_url',
            'text_color_class',
            'get_attendees',
            'get_rsvps',
        ]
