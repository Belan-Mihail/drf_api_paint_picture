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
    

class PlanDetailViewTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        Plan.objects.create(
            owner=user1, 
            plans_title='title1',
            plans_description='description1',
            plans_date='2024-08-14',
            until='False'
        )
        Plan.objects.create(
            owner=user2, 
            plans_title='title2',
            plans_description='description2',
            plans_date='2024-12-03',
            until='True'
        )
    
    def test_can_retrieve_plan_using_valid_id(self):
        response = self.client.get('/plans/1/')
        response2 = self.client.get('/plans/2/')

        self.assertEqual(response.data['plans_title'], 'title1')
        self.assertEqual(response.data['owner'], 'user1')
        self.assertEqual(response.data['until'], False)
        self.assertNotEqual(response.data['owner'], 'user2')
        self.assertEqual(response2.data['plans_title'], 'title2')
        self.assertEqual(response2.data['owner'], 'user2')
        self.assertEqual(response2.data['until'], True)
        self.assertNotEqual(response2.data['owner'], 'user1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
    
    def test_cant_retrieve_plan_using_invalid_id(self):
        response = self.client.get('/plans/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_user_can_update_own_plan(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/plans/1/', {
            'plans_title': 'a new plans title',
            'plans_description': 'a new plans description',
            'plans_date': '2024-12-04',
            'until': 'False'
            })
        plan = Plan.objects.filter(pk=1).first()
        self.assertEqual(plan.plans_description, 'a new plans description')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_user_cant_update_not_own_plan(self):
        self.client.login(username='user1', password='pass')
        response = self.client.put('/plans/2/', {'plans_title': 'a new plan title'})
        plan = Plan.objects.filter(pk=2).first()
        self.assertEqual(plan.plans_title, 'title2')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
