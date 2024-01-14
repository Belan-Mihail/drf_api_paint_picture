from rest_framework import serializers
from .models import Profile



class ProfileSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner


    def validate_content(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Content must contain at least 3 characters')
        return value
    

    class Meta:
        model = Profile

        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'greeting'
        ]