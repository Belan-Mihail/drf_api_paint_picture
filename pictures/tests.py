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


class PictureDetailViewTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        Picture.objects.create(
            owner=user1, title='a title1', description='description1'
        )
        Picture.objects.create(
            owner=user2, title='a title2', description='description2'
        )
    
    def test_can_retrieve_picture_using_valid_id(self):
        response = self.client.get('/pictures/1/')
        response2 = self.client.get('/pictures/2/')

        self.assertEqual(response.data['title'], 'a title1')
        self.assertEqual(response.data['owner'], 'user1')
        self.assertNotEqual(response.data['owner'], 'user2')
        self.assertEqual(response2.data['title'], 'a title2')
        self.assertEqual(response2.data['owner'], 'user2')
        self.assertNotEqual(response2.data['owner'], 'user1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
    
    def test_cant_retrieve_picture_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_user_can_update_own_picture(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/pictures/1/', {'title': 'a new title'})
        picture = Picture.objects.filter(pk=1).first()
        self.assertEqual(picture.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_user_cant_update_not_own_picture(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/pictures/2/', {'title': 'a new title'})
        picture = Picture.objects.filter(pk=2).first()
        self.assertEqual(picture.title, 'a title2')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)