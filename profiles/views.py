from rest_framework import permissions, generics
from .models import Profile
from .serializers import ProfileSerializer
from drf_paintpicture.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListCreateAPIView):
    """
    List all profiles
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().order_by('-created_at')


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve a profile or update it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().order_by('-created_at')