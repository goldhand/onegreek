from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', blank=True)
    title = serializers.WritableField(source='title', blank=True)
    description = serializers.WritableField(source='description', blank=True)
    chapter = serializers.HyperlinkedRelatedField('get_chapter', view_name='chapter-detail', read_only=True)
    chapter_id = serializers.SerializerMethodField('get_chapter_id')
    chapter_title = serializers.Field('get_chapter')
    attend_url = serializers.Field('get_attend_url')
    rsvp_url = serializers.Field('get_rsvp_url')
    text_color_class = serializers.Field('get_status_text_class')
    ctype_id = serializers.SerializerMethodField('get_content_type_id')
    #api_url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = Event
        fields = [
            'id',
            'ctype_id',
            'url',
            'title',
            'slug',
            'chapter',
            'chapter_title',
            'chapter_id',
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
        ]

    def get_chapter_id(self, obj):
        if obj:
            return obj.get_chapter().id
        else:
            return None

    def get_content_type_id(self, obj):
        return ContentType.objects.get_for_model(Event).id


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
    get_rsvps_not_attendees = UserSerializer(many=True)

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
            'get_rsvps_not_attendees',
        ]
