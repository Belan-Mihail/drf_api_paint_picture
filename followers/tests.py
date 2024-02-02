from django.contrib.auth.models import User
from .models import Followers
from rest_framework import status
from rest_framework.test import APITestCase

class FollowersListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        follower = Followers.objects.create(owner=user1, followed=user2)
    
    
    def test_can_list_followers(self):
        user = User.objects.get(username='user1')
        obj = Followers.objects.get(id=1)
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.owner.username, 'user1')
        self.assertTrue(isinstance(obj, Followers))