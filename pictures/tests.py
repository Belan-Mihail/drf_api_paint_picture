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
    
    
    def test_logged_in_user_can_create_picture(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post('/pictures/', {'title': 'a test title1'})
        count = Picture.objects.count()
        obj = Picture.objects.get()
        self.assertEqual(count, 1)
        self.assertEqual(obj.title, 'a test title1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_user_not_logged_in_cant_create_picture(self):
        response = self.client.post('/pictures/', {'title': 'a test title2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
