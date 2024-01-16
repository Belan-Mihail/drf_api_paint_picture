from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Picture
from .serializers import PictureSerializer
from drf_paintpicture.permissions import IsOwnerOrReadOnly

    
class PictureList(generics.ListCreateAPIView):
    """
    List pictures or create a picture if logged in
    """
    serializer_class = PictureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Picture.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
        'picture_category',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PictureDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a picture and edit or delete it if you own it.
    """
    serializer_class = PictureSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Picture.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')
