from rest_framework import generics, permissions
from drf_paintpicture.permissions import IsOwnerOrReadOnly
from .models import Likes
from .serializers import LikesSerializer


class LikesList(generics.ListCreateAPIView):
    """
    List likes or create a like if logged in.
    """
    serializer_class = LikesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Likes.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a likes or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()