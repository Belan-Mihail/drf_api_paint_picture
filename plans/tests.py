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
            owner=user, 
            plans_title='a test title',
            plans_description='a plans_description',
            plans_date='2024-08-14',
            until='False'
        )
        response = self.client.get('/plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.plans_title, 'a test title')
        self.assertEqual(obj.plans_description, 'a plans_description')
        self.assertTrue(isinstance(obj, Plan))
    
    
    def test_logged_in_user_can_create_plan(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post('/plans/', {
            'plans_title': 'a test title',
            'plans_description': 'plans_description',
            'plans_date': '2024-08-14',
            'until': 'False' 
        })
        count = Plan.objects.count()
        obj = Plan.objects.get()
        self.assertEqual(count, 1)
        self.assertEqual(obj.plans_title, 'a test title')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_logged_in_user_cant_create_plan_wit_invalid_date(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post('/plans/', {
            'plans_title': 'a test title',
            'plans_description': 'plans_description',
            'plans_date': '2024-13-32',
            'until': 'False' 
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_logged_in_user_cant_create_plan_wit_invalid_title_lengt(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post('/plans/', {
            'plans_title': 'a'*300,
            'plans_description': 'plans_description',
            'plans_date': '2024-13-32',
            'until': 'False' 
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_logged_in_user_can_create_plan_without_dafault_value(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post('/plans/', {
            'plans_title': 'a test title',
            'plans_description': 'plans_description',
            'plans_date': '2024-08-14',
             
        })
        obj = Plan.objects.get()
        self.assertEqual(obj.until, False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    
