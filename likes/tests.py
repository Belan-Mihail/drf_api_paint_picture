from django.contrib.auth.models import User
from pictures.models import Picture
from .models import Likes
from rest_framework import status
from rest_framework.test import APITestCase


class LikesListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
       user1 = User.objects.create_user(username='user1', password='pass')
       user2 = User.objects.create_user(username='user2', password='pass')
       user3 = User.objects.create_user(username='user3', password='pass')
       picture = Picture.objects.create(owner=user1, title='a title')
       picture_like1 = Likes.objects.create(owner=user1, picture_id=1)
       picture_like2 = Likes.objects.create(owner=user2, picture_id=1)
       

    def test_can_list_picture_likes(self):
        user = User.objects.get(username='user1')
        picture = Picture.objects.get(title='a title')
        picture_like1 = Likes.objects.get(id=1)
        picture_like2 = Likes.objects.get(id=2)
        response = self.client.get('/likes/')
        count = Likes.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 2)
        self.assertEqual(picture_like1.owner.username, 'user1')
        self.assertEqual(picture_like2.owner.username, 'user2')
        self.assertTrue(isinstance(picture_like1, Likes))
        self.assertTrue(isinstance(picture_like2, Likes))
        

    def test_cant_list_likes_using_invalid_url(self):
        response = self.client.get('/like3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
       

    def test_logged_in_user_can_create_like(self):
        self.client.login(username='user3', password='pass')
        picture = Picture.objects.get(id=1)
        response = self.client.post('/likes/', {'picture': 1})
        count = Likes.objects.count()
        picture_likes3 = Likes.objects.get(id=3)
        self.assertEqual(count, 3)
        self.assertEqual(picture_likes3.owner.username, 'user3')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_user_not_logged_in_cant_create_like(self):
        response = self.client.post('/likes/', {'picture': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
class LikesDetailViewTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        user3 = User.objects.create_user(username='user3', password='pass')
        picture = Picture.objects.create(owner=user1, title='a title')
        picture_like1 = Likes.objects.create(owner=user1, picture_id=1)
        picture_like2 = Likes.objects.create(owner=user2, picture_id=1)
        
    
    def test_can_retrieve_likes_using_valid_id(self):
        response = self.client.get('/likes/1/')
        response2 = self.client.get('/likes/2/')

        self.assertEqual(response.data['owner'], 'user1')
        self.assertEqual(response2.data['owner'], 'user2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
    
    def test_cant_retrieve_likes_using_invalid_id(self):
        response = self.client.get('/likes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_user_can_delete_own_likes(self):
        self.client.login(username='user2', password='pass')
        response = self.client.delete('/likes/2/')
        count = Likes.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_user_cant_delete_not_own_like(self):
        self.client.login(username='user1', password='pass')
        response = self.client.delete('/likes/2/')
        count = Likes.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)