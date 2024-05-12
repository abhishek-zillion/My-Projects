from rest_framework import serializers
from library.models import User,Book,BookRequest
from django.contrib.auth import login,logout,authenticate


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password','user_type']
        extra_kwargs={'password':{'write_only':True}}
    
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user
 

class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'
        extra_kwargs={'id':{'read_only':True}}

class BookRequestSerializer(serializers.ModelSerializer):
    book_id=serializers.IntegerField()
        
    class Meta:
        model=BookRequest
        fields=['book_id',]
        
    def create(self,validated_data):
        user=self.context['request'].user
        return BookRequest.objects.create(user=user,**validated_data)

class BookRequestActionSerializer(serializers.Serializer):
    action=serializers.ChoiceField(choices=['APPROVED','REJECTED','REVOKED'])
    request_id=serializers.PrimaryKeyRelatedField(queryset=BookRequest.objects.all())
    
class ReturnBookSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()


class CompleteBookRequestSerializer(serializers.ModelSerializer):
    book=BookSerializer()
    user_name=serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = BookRequest
        fields = ['id', 'book', 'request_date', 'status', 'approval_date', 'due_date', 'returned_date', 'user_name']
        
class RegisteredStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type', 'email']
        
    def to_representation(self, instance):
        if instance.user_type == User.STUDENT:
            return super().to_representation(instance)
        return {}