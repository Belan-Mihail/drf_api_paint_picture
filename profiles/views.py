from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics, filters
from .models import Profile
from .serializers import ProfileSerializer
from drf_paintpicture.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListCreateAPIView):
    """
    List all profiles
    """
    queryset = Profile.objects.annotate(
        pictures_count=Count('owner__picture', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'pictures_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve a profile or update it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        pictures_count=Count('owner__picture', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')