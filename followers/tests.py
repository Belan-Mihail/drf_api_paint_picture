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
    
    
    def test_cant_list_followers_using_invalid_url(self):
        response = self.client.get('/followe4rs/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_logged_in_user_can_following(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post('/followers/', {'owner': 2, 'followed': 1})
        count = Followers.objects.count()
        followers2 = Followers.objects.get(id=2)
        self.assertEqual(count, 2)
        self.assertEqual(followers2.owner.username, 'user2')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_user_not_logged_in_cant_following(self):
        response = self.client.post('/followers/', {'owner': 2, 'followed': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
class FollowersDetailViewTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        follower = Followers.objects.create(owner=user1, followed=user2)
        
    
    def test_can_retrieve_wallitems_using_valid_id(self):
        response = self.client.get('/followers/1/')


        self.assertEqual(response.data['owner'], 'user1')
        self.assertNotEqual(response.data['owner'], 'user2')
        self.assertEqual(response.data['followed'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    
    def test_cant_retrieve_followers_using_invalid_id(self):
        response = self.client.get('/followers/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_user_can_delete_following(self):
        self.client.login(username='user1', password='pass')
        response = self.client.delete('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_user_cant_delete_not_own_following(self):
        self.client.login(username='user2', password='pass')
        response = self.client.delete('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)