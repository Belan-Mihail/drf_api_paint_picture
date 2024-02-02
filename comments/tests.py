from django.contrib.auth.models import User
from pictures.models import Picture
from .models import Comment
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
       user = User.objects.create_user(username='user', password='pass')
       picture1 = Picture.objects.create(owner=user, title='a title')
       picture1_comment = Comment.objects.create(owner=user, picture_id=1, content='comment1')
       picture1_comment2 = Comment.objects.create(owner=user, picture_id=1, content='comment2')

    
    def test_can_list_picture_comments(self):
        user = User.objects.get(username='user')
        picture1 = Picture.objects.get(title='a title')
        picture1_comment = Comment.objects.get(id=1)
        picture1_comment2 = Comment.objects.get(id=2)
        response = self.client.get('/comments/')
        count = Comment.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 2)
        self.assertEqual(picture1_comment.content, 'comment1')
        self.assertEqual(picture1_comment2.content, 'comment2')
        self.assertTrue(isinstance(picture1_comment, Comment))
        
    
    def test_cant_list_comments_using_invalid_url(self):
        response = self.client.get('/comment3s/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
       

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='user', password='pass')
        picture1 = Picture.objects.get(id=1)
        user = User.objects.get(username='user')
        response = self.client.post('/comments/', {'picture': 1, 'content': 'comment3'})
        count = Comment.objects.count()
        picture1_comment3 = Comment.objects.get(id=3)
        self.assertEqual(count, 3)
        self.assertEqual(picture1_comment3.content, 'comment3')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_user_not_logged_in_cant_create_comment(self):
        response = self.client.post('/comments/', {'picture': 1, 'content': 'comment4'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        picture1 = Picture.objects.create(
            owner=user1, title='a title1', description='description1'
        )
        
        picture1_comment = Comment.objects.create(owner=user1, picture_id=1, content='comment1')
        picture1_comment2 = Comment.objects.create(owner=user2, picture_id=1, content='comment2')
        
    
    def test_can_retrieve_comments_using_valid_id(self):
        response = self.client.get('/comments/1/')
        response2 = self.client.get('/comments/2/')

        self.assertEqual(response.data['content'], 'comment1')
        self.assertEqual(response.data['owner'], 'user1')
        self.assertNotEqual(response.data['owner'], 'user2')
        self.assertEqual(response2.data['content'], 'comment2')
        self.assertEqual(response2.data['owner'], 'user2')
        self.assertNotEqual(response2.data['owner'], 'user1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
    
    def test_cant_retrieve_comment_using_invalid_id(self):
        response = self.client.get('/comments/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_user_can_update_own_comment(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/comments/1/', {'content': 'a new content'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'a new content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_user_cant_update_not_own_comment(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/comments/2/', {'content': 'a new content'})
        comment = Comment.objects.filter(pk=2).first()
        self.assertEqual(comment.content, 'comment2')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_user_can_delete_own_comment(self):
        self.client.login(username='user1', password='pass')
        response = self.client.delete('/comments/1/')
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    def test_user_cant_delete_not_own_comment(self):
        self.client.login(username='user1', password='pass')
        response = self.client.delete('/comments/2/')
        count = Comment.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)