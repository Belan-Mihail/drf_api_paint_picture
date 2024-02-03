from django.contrib.auth.models import User
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
        User.objects.create_user(username='user1', password='pass')
        User.objects.create_user(username='user2', password='pass')

    def test_can_list_profiles_and_profiles_are_created_automatically(self):
        response = self.client.get('/profiles/')
        profile1 = Profile.objects.filter(pk=1).first()
        profile2 = Profile.objects.filter(pk=2).first()
        count = Profile.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile1.owner.username, 'user1')
        self.assertEqual(profile2.owner.username, 'user2')
        self.assertEqual(profile1.image, '../default_profile_rg7ho0')
        self.assertEqual(profile2.image, '../default_profile_rg7ho0')
        self.assertTrue(isinstance(profile1, Profile))
        self.assertTrue(isinstance(profile2, Profile))
        self.assertEqual(count, 2)


class ProfileDetailViewTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')

    def test_can_retrieve_profiles_using_valid_id(self):
        response = self.client.get('/profiles/1/')
        response2 = self.client.get('/profiles/2/')
        self.assertEqual(response.data['owner'], 'user1')
        self.assertNotEqual(response.data['owner'], 'user2')
        self.assertEqual(response2.data['owner'], 'user2')
        self.assertNotEqual(response2.data['owner'], 'user1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_profile_using_invalid_id(self):
        response = self.client.get('/profiles/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_profiles(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/profiles/1/', {'name': 'Mike'})
        profile = Profile.objects.filter(pk=1).first()
        self.assertEqual(profile.name, 'Mike')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_not_own_profile(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/profiles/2/', {'name': 'Mike'})
        profile = Profile.objects.filter(pk=2).first()
        self.assertEqual(profile.name, '')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_delete_own_profile(self):
        self.client.login(username='user1', password='pass')
        response = self.client.delete('/profiles/1/')
        count = Profile.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_user_cant_delete_not_own_profile(self):
        self.client.login(username='user1', password='pass')
        response = self.client.delete('/profiles/2/')
        count = Profile.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
