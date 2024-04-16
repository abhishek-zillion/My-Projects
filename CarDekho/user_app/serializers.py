from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self,):
        password = self.validated_data['password']
        password_confirmation = self.validated_data['password_confirmation']
        if password != password_confirmation:

            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists'})
            
        account=User(username=self.validated_data['username'],email=self.validated_data['email'])
        account.set_password(self.validated_data['password'])
        account.save()
    
        