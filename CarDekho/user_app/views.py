from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user_app.serializers import RegisterUserSerializer

class RegistrationView(APIView):
    # http://127.0.0.1:8000/account/register/
    def post(self, request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class LogoutView(APIView):
    def post(self, request):
        
        request.user.auth_token.delete()
        return Response({'msg':'token deleted'},status=204)