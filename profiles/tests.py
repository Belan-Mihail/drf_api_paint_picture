from django.contrib.auth.models import User
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase

class ProfileListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
        User.objects.create_user(username='user1', password='pass')
        User.objects.create_user(username='user2', password='pass')
    
    
    def test_can_list_profiles(self):
        response = self.client.get('/profiles/')
        profile = Profile.objects.filter(pk=2).first()
        count = Profile.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.owner.username, 'user2')
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(count, 2)
