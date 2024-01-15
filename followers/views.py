from rest_framework import generics, permissions
from drf_paintpicture.permissions import IsOwnerOrReadOnly
from .models import Followers
from .serializers import FollowersSerializer


class FollowersList(generics.ListCreateAPIView):
    """
    List followers or create a like if logged in.
    """
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Followers.objects.all()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowersDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a followers or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowersSerializer
    queryset = Followers.objects.all()