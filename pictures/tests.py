from django.contrib.auth.models import User
from .models import Picture
from rest_framework import status
from rest_framework.test import APITestCase

class PictureListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
        User.objects.create_user(username='user1', password='pass')
    
    
    def test_can_list_pictures(self):
        user = User.objects.get(username='user1')
        obj = Picture.objects.create(owner=user, title='a test title')
        response = self.client.get('/pictures/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.title, 'a test title')
        self.assertTrue(isinstance(obj, Picture))
