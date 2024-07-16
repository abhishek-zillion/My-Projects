from pprint import pprint
from rest_framework.test import APITestCase
from library.serializers import *
from library.models import *
# from django.contrib.auth import get_user_model

class TestUserSerializer(APITestCase):
    def test_user_serializer_valid_data(self):
        data={
            'username':'testuser',
            'email':'testuser@gmail.com',
            'password':'testuser',
            'user_type':'LIBRARIAN'
        }
        serializer = UserSignUpSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors,{})
        serializer.save()

        data1 ={
            'username':'testuser',
            'password':'wrongpassword',
        }
        serializer = UserLoginSerializer(data=data1)
        self.assertTrue(serializer.is_valid())
        # self.assertIn('non_field_errors',serializer.errors)
        # self.assertEqual(serializer.errors['non_field_errors'][0],'Incorrect username or password')

