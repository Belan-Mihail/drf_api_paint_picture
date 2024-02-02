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