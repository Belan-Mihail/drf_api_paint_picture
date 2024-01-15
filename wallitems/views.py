from rest_framework import generics, permissions
from drf_paintpicture.permissions import IsOwnerOrReadOnly
from .models import WallItem
from .serializers import WallItemSerializer


class WallItemList(generics.ListCreateAPIView):
    """
    List WallItem or create a comment if logged in.
    """

    serializer_class = WallItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = WallItem.objects.all()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WallItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a Wallitem, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly] 
    serializer_class = WallItemSerializer
    queryset = WallItem.objects.all()