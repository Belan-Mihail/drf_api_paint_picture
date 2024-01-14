from rest_framework import serializers
from .models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """
    Serializers for Picture Model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    profile_greeting = serializers.ReadOnlyField(source='owner.profile.greeting')


    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value


    def validate_description(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Content must contain at least 3 characters')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Picture

        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'title',
            'description', 'image', 'picture_category', 'is_owner', 'profile_greeting', 
        ]
