from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    """
    Serializers for Plan Model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.image.url'
    )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Plan

        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'created_at',
            'updated_at', 'plans_title', 'plans_description',
            'plans_date', 'until',
        ]
