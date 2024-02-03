from django.urls import path
from pictures import views


urlpatterns = [
    path('pictures/', views.PictureList.as_view()),
    path('pictures/<int:pk>/', views.PictureDetail.as_view()),
]
