from django.contrib.auth.models import User
from .models import Plan
from rest_framework import status
from rest_framework.test import APITestCase

class PlanListViewTests(APITestCase):
    # setUp before all tests
    def setUp(self):
        User.objects.create_user(username='user1', password='pass')
    
    
    def test_can_list_plans(self):
        user = User.objects.get(username='user1')
        obj = Plan.objects.create(
            owner=user, plans_title='a test title',
            plans_description='a plans_description',
            plans_date='2024-08-14',
            until='False'
        )
        response = self.client.get('/plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.plans_title, 'a test title')
        self.assertEqual(obj.plans_description, 'a plans_description')
        self.assertTrue(isinstance(obj, Plan))
