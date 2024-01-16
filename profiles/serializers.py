from rest_framework import serializers
from .models import Profile
from followers.models import Followers


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializers for Profile Model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    pictures_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner


    def validate_content(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Content must contain at least 3 characters')
        return value
    
    
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Followers.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None
    

    class Meta:
        model = Profile

        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'greeting', 'is_owner', 'following_id', 'pictures_count',
            'followers_count', 'following_count',
        ]