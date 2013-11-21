from rest_framework import serializers

from .models import PComment as Comment
from events.models import Event

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
        #elif isinstance(value, ''):
        #    return 'Note: ' + value.text
        raise Exception('Unexpected type of content object')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    viewers = serializers.PrimaryKeyRelatedField(many=True)
    content_object = ContentObjectRelatedField()

    class Meta:
        model = Comment
        fields = [
            'url', 'comment',
            'submit_date',
            'viewers',
            'content_object',
        ]
        read_only_fields = [
            'submit_date',
        ]
