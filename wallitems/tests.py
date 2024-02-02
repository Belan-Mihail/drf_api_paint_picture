from django.contrib.auth.models import User
from .models import WallItem
from profiles.models import Profile
from rest_framework import status
from rest_framework.test import APITestCase

class WallItemListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
        user = User.objects.create_user(username='user1', password='pass')
        wallitem = WallItem.objects.create(owner=user, profile_id=1, message='message1')
    
    
    def test_can_list_wallitem(self):
        user = User.objects.get(username='user1')
        obj = WallItem.objects.get(id=1)
        response = self.client.get('/wallitems/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.message, 'message1')
        self.assertTrue(isinstance(obj, WallItem))
