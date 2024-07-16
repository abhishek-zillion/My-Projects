from django.test import TestCase
from library.models import Book, BookRequest, User

# tear_down

class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user', email='test@email.com', password='testpassword')

    def test_user(self):
        expected_data = {
            'username': 'test_user',
            'email': 'test@email.com',
            'password': 'testpassword',
            'user_type': 'STUDENT',
            'login_time': None,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
        actual_data = {
            'username': self.user.username,
            'email': self.user.email,
            'password':  self.user.password,
            'user_type': self.user.user_type,
            'login_time': self.user.login_time,
            'is_active': self.user.is_active,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
        }
        self.assertEqual(self.user.username, 'test_user')
        self.assertFalse(self.user.is_superuser)
        self.assertDictEqual(expected_data, actual_data)
        self. assertIsNotNone(self.user.email)
        self.assertIsNone(self.user.login_time)
        self.assertTrue(hasattr(self.user,'username'))
        self.assertIn(self.user.user_type, [choice[0] for choice in User.USER_TYPE_CHOICES])

    
