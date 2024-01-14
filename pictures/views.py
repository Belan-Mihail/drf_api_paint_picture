from rest_framework import permissions, generics
from .models import Picture
from .serializers import PictureSerializer
from drf_paintpicture.permissions import IsOwnerOrReadOnly

    
class PictureList(generics.ListCreateAPIView):
    """
    List pictures or create a picture if logged in
    """
    serializer_class = PictureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Picture.objects.all().order_by('-created_at')


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PictureDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a picture and edit or delete it if you own it.
    """
    serializer_class = PictureSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Picture.objects.all().order_by('-created_at')
