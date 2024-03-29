from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import WallItem


class WallItemSerializer(serializers.ModelSerializer):
    """
    Serializers for Wallitem Model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def validate_message(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'Message must contain at least 5 characters'
            )
        return value

    class Meta:
        model = WallItem

        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'created_at',
            'updated_at', 'message', 'profile',
        ]


class WallItemDetailSerializer(WallItemSerializer):
    """
    Serializer for the WallItems model used in Detail view
    """
    profile = serializers.ReadOnlyField(source='profile.id')
