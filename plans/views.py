from rest_framework import generics, permissions
from drf_paintpicture.permissions import IsOwnerOrReadOnly
from .models import Plan
from .serializers import PlanSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PlanList(generics.ListCreateAPIView):
    """
    List Plan or create plan.
    """

    serializer_class = PlanSerializer
    permission_classes = [IsOwnerOrReadOnly] 
    queryset = Plan.objects.all()
    
    
    filter_backends = [
        DjangoFilterBackend
    ]
    
    filterset_fields = [
        'owner__profile',
    ]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlanDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a Plan, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly] 
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()