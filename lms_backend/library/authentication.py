from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from library.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class CustomBookAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Your authentication logic specific to the book view goes here
        # For example, you can check for a custom header or query parameter
        # Retrieve the token from the request
        token = request.META.get('HTTP_CUSTOM_BOOK_TOKEN')
        
        
        if not token:
            # If token is not provided, raise AuthenticationFailed
            raise AuthenticationFailed('Authentication credentials were not provided for book view.')
        
        # Authenticate the user based on the token
        try:
            user = User.objects.get(auth_token=token)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid token for book view.')
        
        return (user, None)  # Return a tuple of (user, None) to indicate successful authentication


