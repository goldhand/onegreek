from rest_framework import serializers

from .models import RestComment
from events.models import Event
from chapters.models import Chapter


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """

    def to_native(self, value):
        """
        Serialize content objects to a simple textual representation.
        """
        if isinstance(value, Event):
            return value.get_absolute_url()
        if isinstance(value, Chapter):
            return value.get_absolute_url()
        #elif isinstance(value, ''):
        #    return 'Note: ' + value.text
        raise Exception('Unexpected type of content object')


class RestCommentSerializer(serializers.HyperlinkedModelSerializer):
    #viewers = serializers.PrimaryKeyRelatedField(many=True)
    #content_object = ContentObjectRelatedField()
    content_type = serializers.PrimaryKeyRelatedField(source='content_type')
    name = serializers.Field(source='name')
    profile_image_url = serializers.SerializerMethodField('get_profile_image_url')
    #site = serializers.PrimaryKeyRelatedField()
    content_object_url = serializers.Field(source='get_content_object_url')
    content_object = serializers.Field(source='content_object')
    user = serializers.PrimaryKeyRelatedField('user')

    class Meta:
        model = RestComment
        fields = [
            'user',
            'name',
            'comment',
            'url',
            'profile_image_url',
            'submit_date',
            'content_type',
            'object_pk',
            'content_object_url',
            'content_object',
            #'timestamp',
            #'security_hash',
        ]
        read_only_fields = [
            'submit_date',
            #'content_type',
            #'object_pk',
            #'content_object',
            #'timestamp',
            #'security_hash',
        ]

    def get_profile_image_url(self, obj):
        if obj:
            return obj.user.profile_image_url()
        else:
            return None
