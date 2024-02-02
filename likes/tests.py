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
