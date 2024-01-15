from django.urls import path
from plans import views


urlpatterns = [
    path('plans/', views.PlanList.as_view()),
    path('plans/<int:pk>/', views.PlanDetail.as_view()),
]