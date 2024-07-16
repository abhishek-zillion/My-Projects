from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from library.models import *
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from django.contrib.auth import get_user_model


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()  

    def test_user_signup(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'user_type': 'LIBRARIAN',
        }

        url = reverse('signup')

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)  
        self.assertIn('email', response.data)
        self.assertNotIn('password', response.data)

    def test_user_login(self):
        # correct login
        # incorrect login
        # incomplete login

        self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testemail@example.com',
            'user_type': 'LIBRARIAN',
        }, format='json')

        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'user_type': 'LIBRARIAN',
        }
        response = self.client.post(
            reverse('login'), data=login_data, format='json')
        self.assertNotIn('password', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['token']

        incorrect_login_data = {
            'username': 'testuser',
            'password': 'password',
        }
        response = self.client.post(
            reverse('login'), data=incorrect_login_data, format='json')
        self.assertIsInstance(token, str)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['message'], 'Unable to login with provided credentials.'.lower())

        incomplete_login_data = {
            'username': 'testuser'
        }
        response = self.client.post(
            reverse('login'), data=incomplete_login_data, format='json')
        self.assertTrue('password' in response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        return token

    def test_token_verfication(self):
        token = self.test_user_login()
        url = reverse('allbooks')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        token = self.test_user_login()
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(url)
        self.assertEqual(response.data['message'], 'Logout successful')


class AllBooksViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('allbooks')
        self.user = get_user_model()
        
        self.librarian = self.user.objects.create_user(username='testlibrarian', email='testlibrarian@gmail.com', password='password', user_type='LIBRARIAN')
        self.student = self.user.objects.create_user(username='teststudent', email='teststudent@gmail.com', password='password', user_type='STUDENT')

        self.book1 = Book.objects.create(title='testbook1', author='testauthor1', stock=10, status='AVAILABLE')
        self.book2 = Book.objects.create(title='testbook2', author='testauthor2', stock=10, status='AVAILABLE')
        
    
    def authenticate_user(self,user):
        login_data = {
            'username': user.username,
            'password': 'password',            
        }
        response=self.client.post(reverse('login'),data=login_data , format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=token)
        print(token)
        return token
    
    def test_get_all_books_librarian(self):
        self.authenticate_user(self.librarian)
        
        response = self.client.get(self.url)
        self.assertTrue(isinstance(response.data,list))
        
        expected_keys = ['id', 'title', 'authr']
