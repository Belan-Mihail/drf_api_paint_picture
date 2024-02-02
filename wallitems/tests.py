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
    
    
    def test_cant_list_wallitems_using_invalid_url(self):
        response = self.client.get('/walli45tems/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_logged_in_user_can_create_wallitem(self):
        self.client.login(username='user1', password='pass')
        wallitem = WallItem.objects.get(id=1)
        user = User.objects.get(username='user1')
        response = self.client.post('/wallitems/', {'profile': 1, 'message': 'hello'})
        count = WallItem.objects.count()
        wallitem2 = WallItem.objects.get(id=2)
        self.assertEqual(count, 2)
        self.assertEqual(wallitem2.message, 'hello')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_user_not_logged_in_cant_create_wallitem(self):
        response = self.client.post('/wallitems/', {'profile': 1, 'message': 'I cant create'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WallItemDetailViewTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        wallitem = WallItem.objects.create(owner=user1, profile_id=1, message='message1')
        wallitem2 = WallItem.objects.create(owner=user2, profile_id=2, message='message2')
        
    
    def test_can_retrieve_comments_using_valid_id(self):
        response = self.client.get('/wallitems/1/')
        response2 = self.client.get('/wallitems/2/')

        self.assertEqual(response.data['message'], 'message1')
        self.assertEqual(response.data['owner'], 'user1')
        self.assertNotEqual(response.data['owner'], 'user2')
        self.assertEqual(response2.data['message'], 'message2')
        self.assertEqual(response2.data['owner'], 'user2')
        self.assertNotEqual(response2.data['owner'], 'user1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)