from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializers for Comment Model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

# update data formatting
    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

# update data formatting
    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

# validate comments content
    def validate_content(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Content must contain at least 6 characters')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Comment

        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'picture',
            'content', 'is_owner', 
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model used in Detail view
    """
    picture = serializers.ReadOnlyField(source='picture.id') 